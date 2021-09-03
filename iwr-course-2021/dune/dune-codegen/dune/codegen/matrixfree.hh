#ifndef DUNE_CODEGEN_MATRIXFREE_HH
#define DUNE_CODEGEN_MATRIXFREE_HH

#include <iostream>

#include <dune/pdelab/backend/istl.hh>

#include <dune/codegen/matrixfreeistlbackends.hh>
#include <dune/codegen/matrixfreenewton.hh>

namespace Dune{
  namespace PDELab{


    template <typename GO, typename V, typename Preconditioner>
    void solveMatrixFree(GO& go, V& x, Preconditioner& pre){
      using ISTLOnTheFlyOperator = Dune::PDELab::OnTheFlyOperator<V,V,GO>;
      ISTLOnTheFlyOperator opb(go);
      Dune::BiCGSTABSolver<V> solverb(opb, pre, 1E-10, 5000, 2);
      Dune::InverseOperatorResult stat;
      // evaluate residual w.r.t initial guess
      using TrialGridFunctionSpace = typename GO::Traits::TrialGridFunctionSpace;
      using W = Dune::PDELab::Backend::Vector<TrialGridFunctionSpace,typename V::ElementType>;
      W r(go.testGridFunctionSpace(),0.0);
      go.residual(x,r);
      // solve the jacobian system
      V z(go.trialGridFunctionSpace(),0.0);
      solverb.apply(z,r,stat);
      x -= z;
    }


    template <typename GO, typename V>
    void solveMatrixFree(GO& go, V& x){
      using LinearSolver = ISTLBackend_SEQ_MatrixFree_BCGS_Richardson<GO>;
      LinearSolver ls(go, 5000, 2);
      // evaluate residual w.r.t initial guess
      using TrialGridFunctionSpace = typename GO::Traits::TrialGridFunctionSpace;
      using W = Dune::PDELab::Backend::Vector<TrialGridFunctionSpace,typename V::ElementType>;
      W r(go.testGridFunctionSpace(),0.0);
      go.residual(x,r);
      // solve the jacobian system
      V z(go.trialGridFunctionSpace(),0.0);
      ls.apply(z,r,1e-10);
      x -= z;
    }


    template <typename GO, typename V>
    void solveNonlinearMatrixFree(GO& go, V& x ){
      // Matrix free linear solver
      using LinearSolver = ISTLBackend_SEQ_MatrixFree_BCGS_Richardson<GO>;
      LinearSolver ls(go);

      // Solve nonlinear system with matrix free newton
      using SNP = MatrixFreeNewton<GO, LinearSolver, V>;
      SNP snp(go, x, ls);
      snp.apply();
    }

  } // namespace PDELab
} // namespace Dune

#endif
