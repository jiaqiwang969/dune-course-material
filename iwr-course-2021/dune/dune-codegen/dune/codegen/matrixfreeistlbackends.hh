#ifndef DUNE_CODEGEN_MATRIXFREEISTLBACKENDS_HH
#define DUNE_CODEGEN_MATRIXFREEISTLBACKENDS_HH
namespace Dune {
  namespace PDELab {


    /** \brief Application of jacobian from nonlinear problems.

        \tparam X  Trial vector.
        \tparam Y  Test vector.
        \tparam GO Grid operator implementing the operator application.
    */
    template<typename X, typename Y, typename GO>
    class NonlinearOnTheFlyOperator : public Dune::LinearOperator<X,Y>
    {
    public :
      typedef X domain_type;
      typedef Y range_type;
      typedef typename X::field_type field_type;

      NonlinearOnTheFlyOperator(const GO& go)
        : go_(go)
        , u_(static_cast<X*>(0))
      {}

      //! Set position of jacobian. This is different to linear problems.
      //! Must be called before both apply() and applyscaleadd().
      void setLinearizationPoint(const X& u)
      {
        u_ = &u;
      }

      virtual void apply(const X& x, Y& y) const
      {
        y = 0.0;
        go_.nonlinear_jacobian_apply(*u_,x,y);
      }

      virtual void applyscaleadd(field_type alpha, const X& x, Y& y) const
      {
        Y temp(y);
        temp = 0.0;
        go_.nonlinear_jacobian_apply(*u_,x,temp);
        y.axpy(alpha,temp);
      }

      virtual Dune::SolverCategory::Category category() const
      {
        return Dune::SolverCategory::sequential;
      }

    private :
      const GO& go_;
      const X* u_;
    };

  } // end namespace PDELab
} // end namespace Dune
#endif
