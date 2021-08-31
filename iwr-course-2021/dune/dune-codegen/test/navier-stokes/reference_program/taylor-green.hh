#ifndef TAYLOR_GREEN_HH
#define TAYLOR_GREEN_HH

//===============================================================
// Define parameter functions f,g,j and \partial\Omega_D/N
//===============================================================

// constraints parameter class for selecting boundary condition type
class BCTypeParamGlobalDirichlet
{
public :
  typedef Dune::PDELab::StokesBoundaryCondition BC;

  struct Traits
  {
    typedef BC::Type RangeType;
  };

  BCTypeParamGlobalDirichlet() {}

  template<typename I>
  inline void evaluate (const I & intersection,   /*@\label{bcp:name}@*/
                        const Dune::FieldVector<typename I::ctype, I::dimension-1> & coord,
                        BC::Type& y) const
  {
    y = BC::VelocityDirichlet;
  }

  template<typename T>
  void setTime(T t){
  }
};


template<typename GV, typename RF, int dim>
class TaylorGreenVelocity :
  public Dune::PDELab::AnalyticGridFunctionBase<
  Dune::PDELab::AnalyticGridFunctionTraits<GV,RF,dim>,
  TaylorGreenVelocity<GV,RF,dim> >
{
public:
  typedef Dune::PDELab::AnalyticGridFunctionTraits<GV,RF,dim> Traits;
  typedef Dune::PDELab::AnalyticGridFunctionBase<Traits,TaylorGreenVelocity<GV,RF,dim> > BaseT;

  typedef typename Traits::DomainType DomainType;
  typedef typename Traits::RangeType RangeType;

  TaylorGreenVelocity(const GV & gv, const Dune::ParameterTree& params) : BaseT(gv)
  {
    mu = params.get<RF>("mu");
    rho = params.get<RF>("rho");
    time = 0.0;
  }

  inline void evaluateGlobal(const DomainType & x, RangeType & y) const
  {
    // TODO Get mu and rho from somewhere else!
    RF pi = 3.14159265358979323846;
    RF nu = mu/rho;
    y[0] = -exp(-2.0*pi*pi*nu*time)*cos(pi*x[0])*sin(pi*x[1]);
    y[1] = exp(-2.0*pi*pi*nu*time)*sin(pi*x[0])*cos(pi*x[1]);
  }

  template <typename T>
  void setTime(T t){
    time = t;
  }

private:
  RF rho;
  RF mu;
  RF time;
};


template<typename GV, typename RF>
class TaylorGreenPressure
  : public Dune::PDELab::AnalyticGridFunctionBase<
  Dune::PDELab::AnalyticGridFunctionTraits<GV,RF,1>,
  TaylorGreenPressure<GV,RF> >
{
public:
  typedef Dune::PDELab::AnalyticGridFunctionTraits<GV,RF,1> Traits;
  typedef Dune::PDELab::AnalyticGridFunctionBase<Traits,TaylorGreenPressure<GV,RF> > BaseT;

  typedef typename Traits::DomainType DomainType;
  typedef typename Traits::RangeType RangeType;

  TaylorGreenPressure (const GV& gv, const Dune::ParameterTree& params) : BaseT(gv)
  {
    mu = params.get<RF>("mu");
    rho = params.get<RF>("rho");
    time = 0.0;
  }

  inline void evaluateGlobal (const typename Traits::DomainType& x,
                              typename Traits::RangeType& y) const
  {
    RF pi = 3.14159265358979323846;
    RF nu = mu/rho;
    y = -0.25*rho*exp(-4.0*pi*pi*nu*time)*(cos(2.0*pi*x[0])+cos(2.0*pi*x[1]));
  }

  template<typename T>
  void setTime(T t){
    time = t;
  }

private:
  RF rho;
  RF mu;
  RF time;
};



template<typename GV, typename RF, std::size_t dim_range>
class ZeroVectorFunction :
  public Dune::PDELab::AnalyticGridFunctionBase<
  Dune::PDELab::AnalyticGridFunctionTraits<GV,RF,dim_range>,
  ZeroVectorFunction<GV,RF,dim_range> >,
  public Dune::PDELab::InstationaryFunctionDefaults
{
public:
  typedef Dune::PDELab::AnalyticGridFunctionTraits<GV,RF,dim_range> Traits;
  typedef Dune::PDELab::AnalyticGridFunctionBase<Traits, ZeroVectorFunction> BaseT;

  typedef typename Traits::DomainType DomainType;
  typedef typename Traits::RangeType RangeType;

  ZeroVectorFunction(const GV & gv) : BaseT(gv) {}

  inline void evaluateGlobal(const DomainType & x, RangeType & y) const
  {
    y=0;
  }
};

template<typename GV, typename RF>
class ZeroScalarFunction
  : public ZeroVectorFunction<GV,RF,1>
{
public:

  ZeroScalarFunction(const GV & gv) : ZeroVectorFunction<GV,RF,1>(gv) {}

};

#endif
