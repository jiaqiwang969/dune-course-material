#ifndef DUNE_CODEGEN_SUMFACT_ONEDQUADRATURE_HH
#define DUNE_CODEGEN_SUMFACT_ONEDQUADRATURE_HH


#include <dune/geometry/quadraturerules.hh>


//! Return sorted quadrature points and weight
template <typename RF, typename DF, int m>
void onedQuadraturePointsWeights(RF (&qp)[m], RF (&qw)[m]){
  // Get oned quadrature rule
  const int order = 2*m-2;
  const auto& rule = Dune::QuadratureRules<DF, 1>::rule(Dune::GeometryType::cube,order);

  // Save quadrature points and weight in qp and qp
  size_t count=0;
  for (const auto& ip : rule) {
    size_t group=count/2;
    size_t member=count%2;
    size_t newj;
    if (member==1) newj=group;
    else newj=m-1-group;
    qp[newj] = ip.position()[0];
    qw[newj] = ip.weight();
    // std::cout << "j=" << count << " newj=" << newj
    //           << " qp=" << ip.position()[0]
    //           << " qw=" << ip.weight()
    //           << std::endl;
    count++;
  } // end 1D quadrature loop
  // Order 1D quadrature points lexicographically
  for (size_t j=0; j<m/2; j++){
    if (qp[j]>DF(0.5)){
      RF temp=qp[j];
      qp[j] = qp[m-1-j];
      qp[m-1-j] = temp;
      temp=qw[j];
      qw[j] = qw[m-1-j];
      qw[m-1-j] = temp;
    }
  }
}

#endif
