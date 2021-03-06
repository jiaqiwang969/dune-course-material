// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#include "config.h"

#define DISABLE_AMG_DIRECTSOLVER 1

#include <dune/common/parallel/mpihelper.hh>
#include <dune/common/parametertree.hh>
#include <dune/common/parametertreeparser.hh>
#include <dune/common/simd/loop.hh>

#include <dune/istl/bvector.hh>
#include <dune/istl/bcrsmatrix.hh>
#include <dune/istl/operators.hh>
#include <dune/istl/solverfactory.hh>
#include <dune/istl/paamg/test/anisotropic.hh>

// direct solvers
#include <dune/istl/cholmod.hh>
#include <dune/istl/ldl.hh>
#include <dune/istl/spqr.hh>
#include <dune/istl/superlu.hh>
#include <dune/istl/umfpack.hh>

// preconditioners
#include <dune/istl/preconditioners.hh>
#include <dune/istl/paamg/amg.hh>

// solvers
#include <dune/istl/solvers.hh>

#include <dune/istl/test/laplacian.hh>

using Vector = Dune::BlockVector<Dune::FieldVector<Dune::LoopSIMD<double, 4>, 2>>;

template<class V>
struct MatrixBlock{
  typedef V type;
};
template<class T, int n>
struct MatrixBlock<Dune::FieldVector<T,n>>{
  typedef Dune::FieldMatrix<Dune::Simd::Scalar<T>,n,n> type;
};
using Matrix = Dune::BCRSMatrix<typename MatrixBlock<Dune::FieldVector<Dune::LoopSIMD<double, 4>, 2>>::type>;

template<class Comm>
void testSeq(const Dune::ParameterTree& config, Comm c){
  if(c.rank() == 0){
    Matrix mat;
    int N = config.get("N", 10);
    setupLaplacian(mat, N);
    Vector x(mat.M()), b(mat.N());

    using Operator = Dune::MatrixAdapter<Matrix, Vector, Vector>;
    std::shared_ptr<Operator> op = std::make_shared<Operator>(mat);

    for(std::string test : config.getSubKeys()){
      Dune::ParameterTree solverConfig = config.sub(test);
      std::cout << " ============== " << test << " ============== " << std::endl;
      try{
        std::shared_ptr<Dune::InverseOperator<Vector, Vector>> solver = getSolverFromFactory(op, solverConfig);
        x = 0;
        b = 1;
        Dune::InverseOperatorResult res;
        solver->apply(x,b,res);
        if(!res.converged)
          DUNE_THROW(Dune::Exception, test << " not converged!");
      }catch(Dune::UnsupportedType& e){
        std::cout << e.what() << std::endl;
      }
    }
  }
}

int main(int argc, char** argv){
  auto& mpihelper = Dune::MPIHelper::instance(argc, argv);
  Dune::ParameterTree config;
  Dune::ParameterTreeParser::readINITree("solverfactorytest.ini", config);
  Dune::ParameterTreeParser::readOptions(argc, argv, config);

  Dune::initSolverFactories<Matrix,Vector,Vector>();

  std::cout << std::endl << " Testing sequential tests... " << std::endl;
  testSeq(config.sub("sequential"), mpihelper.getCollectiveCommunication());
  // std::cout << std::endl << " Testing overlapping tests... " << std::endl;
  // testOverlapping(config.sub("overlapping"), mpihelper.getCollectiveCommunication());
  //   std::cout << std::endl << " Testing nonoverlapping tests... " << std::endl;
  // testNonoverlapping(config.sub("nonoverlapping"), mpihelper.getCollectiveCommunication());
  return 0;
}
