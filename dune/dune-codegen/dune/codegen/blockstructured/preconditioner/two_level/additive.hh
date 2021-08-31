#ifndef NEUMANN_NEUMANN_PRECONDITIONER_ADDITIVE_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_ADDITIVE_HH

#include <dune/istl/preconditioner.hh>

template<typename X, typename Y>
class AdditiveTwoLevel : public Dune::Preconditioner<X, Y>{
public:
  //! The type of the domain of the operator.
  typedef X domain_type;
  //! The type of the range of the operator.
  typedef Y range_type;
  //! The field type of the operator.
  typedef typename X::field_type field_type;

  AdditiveTwoLevel(Dune::Preconditioner<X, Y>& f_prec_, Dune::Preconditioner<X, Y>& c_prec_)
      : f_prec(f_prec_), c_prec(c_prec_) { }

  void pre (X& x, Y& b) override {}

  void apply (X& v, const Y& d) override {
    X w(v);
    // v = B_f * d
    v = 0;
    f_prec.apply(v, d);

    // w = B_c * r
    w = 0;
    c_prec.apply(w, d);

    v += w;
  }

  void post (X& x) override {}

  [[nodiscard]] Dune::SolverCategory::Category category() const override { return Dune::SolverCategory::sequential; }

private:
  Dune::Preconditioner<X, Y>& f_prec;
  Dune::Preconditioner<X, Y>& c_prec;
};


#endif //NEUMANN_NEUMANN_PRECONDITIONER_ADDITIVE_HH
