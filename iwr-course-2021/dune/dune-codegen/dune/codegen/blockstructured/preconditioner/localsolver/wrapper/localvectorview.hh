#ifndef NEUMANN_NEUMANN_PRECONDITIONER_LOCALVECTORVIEW_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_LOCALVECTORVIEW_HH

#include <dune/pdelab/backend/interface.hh>

struct LFS{
  template<typename I>
  auto localIndex(const I i) const { return i;}
};

template<typename V>
class LocalVectorView{
public:
  explicit LocalVectorView(V& data_) : data(data_) {}

  template<typename LFS>
  decltype(auto) operator()(const LFS& lfs, std::size_t i)
  {
    return Dune::PDELab::Backend::native(data)[lfs.localIndex(i)];
  }

  template<typename LFS>
  decltype(auto) operator()(const LFS& lfs, std::size_t i) const
  {
    return Dune::PDELab::Backend::native(data)[lfs.localIndex(i)];
  }
  template<typename LFS>
  void accumulate(const LFS& lfs, std::size_t i, typename V::value_type v)
  {
    Dune::PDELab::Backend::native(data)[lfs.localIndex(i)] += v;
  }

  LocalVectorView<V>& container() { return *this; }

  double weight() const { return 1.; }
private:
  V& data;
};

template<typename V>
class LocalMatrixNormView{
public:
  explicit LocalMatrixNormView(V& data_) : data(data_) {}

  template<typename LFS>
  void accumulate(const LFS& lfsu, const std::size_t i, const LFS& lfsv, const std::size_t j, typename V::field_type v)
  {
    Dune::PDELab::Backend::native(data)[lfsu.localIndex(i)] += std::abs(v);
  }

private:
  V& data;
};

template<typename X>
auto create_zero(const X& x) {
  using Dune::PDELab::Backend::native;
  X zero(x.size());
  std::fill(begin(native(zero)), end(native(zero)), 0.);
  return zero;
}

#endif //NEUMANN_NEUMANN_PRECONDITIONER_LOCALVECTORVIEW_HH
