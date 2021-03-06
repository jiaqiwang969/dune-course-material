// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_TYPETREE_TRAVERSAL_HH
#define DUNE_TYPETREE_TRAVERSAL_HH

#if HAVE_RVALUE_REFERENCES
#include <utility>
#endif

#include <dune/common/std/type_traits.hh>
#include <dune/common/std/utility.hh>
#include <dune/common/std/type_traits.hh>
#include <dune/common/hybridutilities.hh>

#include <dune/typetree/childextraction.hh>
#include <dune/typetree/nodetags.hh>
#include <dune/typetree/treepath.hh>
#include <dune/typetree/visitor.hh>

namespace Dune {
  namespace TypeTree {

    /** \addtogroup Tree Traversal
     *  \ingroup TypeTree
     *  \{
     */


    namespace Detail {

      // This is a constexpr version of the ternery operator c?t1:t1.
      // In contrast to the latter the type of t1 and t2 can be different.
      // Notice that std::conditional would not do the trick, because
      // it only selects between types.
      template<bool c, class T1, class T2,
        std::enable_if_t<c, int> = 0>
      constexpr auto conditionalValue(T1&& t1, T2&& t2) {
        return std::forward<T1>(t1);
      }

      template<bool c, class T1, class T2,
        std::enable_if_t<not c, int> = 0>
      constexpr auto conditionalValue(T1&& t1, T2&& t2) {
        return std::forward<T2>(t2);
      }

      template<class Tree, TreePathType::Type pathType, class Prefix,
        std::enable_if_t<Tree::isLeaf, int> = 0>
      constexpr auto leafTreePathTuple(Prefix prefix)
      {
        return std::make_tuple(prefix);
      }

      template<class Tree, TreePathType::Type pathType, class Prefix,
        std::enable_if_t<not Tree::isLeaf, int> = 0>
      constexpr auto leafTreePathTuple(Prefix prefix);

      template<class Tree, TreePathType::Type pathType, class Prefix, std::size_t... indices,
        std::enable_if_t<(Tree::isComposite or (Tree::isPower and (pathType!=TreePathType::dynamic))), int> = 0>
      constexpr auto leafTreePathTuple(Prefix prefix, Std::index_sequence<indices...>)
      {
        return std::tuple_cat(Detail::leafTreePathTuple<TypeTree::Child<Tree,indices>, pathType>(Dune::TypeTree::push_back(prefix, Dune::index_constant<indices>{}))...);
      }

      template<class Tree, TreePathType::Type pathType, class Prefix, std::size_t... indices,
        std::enable_if_t<(Tree::isPower and (pathType==TreePathType::dynamic)), int> = 0>
      constexpr auto leafTreePathTuple(Prefix prefix, Std::index_sequence<indices...>)
      {
        return std::tuple_cat(Detail::leafTreePathTuple<TypeTree::Child<Tree,indices>, pathType>(Dune::TypeTree::push_back(prefix, indices))...);
      }

      template<class Tree, TreePathType::Type pathType, class Prefix,
        std::enable_if_t<not Tree::isLeaf, int>>
      constexpr auto leafTreePathTuple(Prefix prefix)
      {
        return Detail::leafTreePathTuple<Tree, pathType>(prefix, Dune::Std::make_index_sequence<Tree::degree()>{});
      }

      /* The signature is the same as for the public applyToTree
       * function in Dune::Typetree, despite the additionally passed
       * treePath argument. The path passed here is associated to
       * the tree and the relative paths of the children (wrt. to tree)
       * are appended to this.  Hence the behavior of the public function
       * is resembled by passing an empty treePath.
       */

      /*
       * This is the overload for leaf traversal
       */
      template<class T, class TreePath, class V,
        std::enable_if_t<std::decay_t<T>::isLeaf, int> = 0>
      void applyToTree(T&& tree, TreePath treePath, V&& visitor)
      {
        visitor.leaf(tree, treePath);
      }

      /*
       * This is the general overload doing child traversal.
       */
      template<class T, class TreePath, class V,
        std::enable_if_t<not std::decay_t<T>::isLeaf, int> = 0>
      void applyToTree(T&& tree, TreePath treePath, V&& visitor)
      {
        // Do we really want to take care for const-ness of the Tree
        // when instantiating VisitChild below? I'd rather expect this:
        // using Tree = std::decay_t<T>;
        // using Visitor = std::decay_t<V>;
        using Tree = std::remove_reference_t<T>;
        using Visitor = std::remove_reference_t<V>;
        visitor.pre(tree, treePath);

        // Use statically encoded degree unless tree
        // is a power node and dynamic traversal is requested.
        constexpr auto useDynamicTraversal = (Tree::isPower and Visitor::treePathType==TreePathType::dynamic);
        auto degree = conditionalValue<useDynamicTraversal>(Tree::degree(), Dune::index_constant<Tree::degree()>{});

        auto indices = Dune::range(degree);
        Dune::Hybrid::forEach(indices, [&](auto i) {
          auto childTreePath = Dune::TypeTree::push_back(treePath, i);
          auto&& child = tree.child(i);
          using Child = std::decay_t<decltype(child)>;

          visitor.beforeChild(tree, child, treePath, i);

          // This requires that visiotor.in(...) can always be instantiated,
          // even if there's a single child only.
          if (i>0)
            visitor.in(tree, treePath);
          static const auto visitChild = Visitor::template VisitChild<Tree,Child,TreePath>::value;
          Dune::Hybrid::ifElse(Dune::Std::bool_constant<visitChild>{}, [&] (auto id) {
            applyToTree(child, childTreePath, visitor);
          });

          visitor.afterChild(tree, child, treePath, i);
        });
        visitor.post(tree, treePath);
      }



      /* Traverse tree and visit each node. The signature is the same
       * as for the public forEachNode function in Dune::Typtree,
       * despite the additionally passed treePath argument. The path
       * passed here is associated to the tree and the relative
       * paths of the children (wrt. to tree) are appended to this.
       * Hence the behavior of the public function is resembled
       * by passing an empty treePath.
       */
      template<class Tree, class TreePath, class PreFunc, class LeafFunc, class PostFunc>
      void forEachNode(Tree&& tree, TreePath treePath, PreFunc&& preFunc, LeafFunc&& leafFunc, PostFunc&& postFunc)
      {
        using TreeType = std::decay_t<Tree>;
        Dune::Hybrid::ifElse(Dune::Std::bool_constant<TreeType::isLeaf>{}, [&] (auto id) {
          // If we have a leaf tree just visit it using the leaf function.
          leafFunc(id(tree), treePath);
        }, [&] (auto id) {
          // Otherwise visit the tree with the pre function,
          // visit all children using a static loop, and
          // finally visit the tree with the post function.
          preFunc(id(tree), treePath);
          auto indices = Dune::Std::make_index_sequence<TreeType::degree()>{};
          Dune::Hybrid::forEach(indices, [&](auto i) {
            auto childTreePath = Dune::TypeTree::push_back(treePath, i);
            forEachNode(id(tree).child(i), childTreePath, preFunc, leafFunc, postFunc);
          });
          postFunc(id(tree), treePath);
        });
      }

    } // namespace Detail


    // ********************************************************************************
    // Public Interface
    // ********************************************************************************

    /**
     * \brief Create tuple of tree paths to leafs
     *
     * This creates a tuple of HybridTreePath objects refering to the
     * leaf nodes in the tree. The generated tree paths are always
     * HybridTreePath instances. If pathType is TreePathType::dynamic
     * then path entries for power nodes are of type std::size_t.
     * For all other nodes and if pathType is not TreePathType::dynamic,
     * the entries are instances of Dune::index_constant.
     *
     * \tparam Tree Type of tree to generate tree paths for
     * \tparam pathType Type of paths to generate
     */
    template<class Tree, TreePathType::Type pathType=TreePathType::dynamic>
    constexpr auto leafTreePathTuple()
    {
      return Detail::leafTreePathTuple<std::decay_t<Tree>, pathType>(hybridTreePath());
    }

    //! Apply visitor to TypeTree.
    /**
     * \code
     #include <dune/typetree/traversal.hh>
     * \endcode
     * This function applies the given visitor to the given tree. Both visitor and tree may be const
     * or non-const (if the compiler supports rvalue references, they may even be a non-const temporary).
     *
     * \note The visitor must implement the interface laid out by DefaultVisitor (most easily achieved by
     *       inheriting from it) and specify the required type of tree traversal (static or dynamic) by
     *       inheriting from either StaticTraversal or DynamicTraversal.
     *
     * \param tree    The tree the visitor will be applied to.
     * \param visitor The visitor to apply to the tree.
     */
    template<typename Tree, typename Visitor>
    void applyToTree(Tree&& tree, Visitor&& visitor)
    {
      Detail::applyToTree(tree, hybridTreePath(), visitor);
    }

    /**
     * \brief Traverse tree and visit each node
     *
     * All passed callback functions are called with the
     * node and corresponding treepath as arguments.
     *
     * \param tree The tree to traverse
     * \param preFunc This function is called for each inner node before visiting its children
     * \param leafFunc This function is called for each leaf node
     * \param postFunc This function is called for each inner node after visiting its children
     */
    template<class Tree, class PreFunc, class LeafFunc, class PostFunc>
    void forEachNode(Tree&& tree, PreFunc&& preFunc, LeafFunc&& leafFunc, PostFunc&& postFunc)
    {
      Detail::forEachNode(tree, hybridTreePath(), preFunc, leafFunc, postFunc);
    }

    /**
     * \brief Traverse tree and visit each node
     *
     * All passed callback functions are called with the
     * node and corresponding treepath as arguments.
     *
     * \param tree The tree to traverse
     * \param innerFunc This function is called for each inner node before visiting its children
     * \param leafFunc This function is called for each leaf node
     */
    template<class Tree, class InnerFunc, class LeafFunc>
    void forEachNode(Tree&& tree, InnerFunc&& innerFunc, LeafFunc&& leafFunc)
    {
      auto nop = [](auto&&... args) {};
      forEachNode(tree, innerFunc, leafFunc, nop);
    }

    /**
     * \brief Traverse tree and visit each node
     *
     * The passed callback function is called with the
     * node and corresponding treepath as arguments.
     *
     * \param tree The tree to traverse
     * \param nodeFunc This function is called for each node
     */
    template<class Tree, class NodeFunc>
    void forEachNode(Tree&& tree, NodeFunc&& nodeFunc)
    {
      forEachNode(tree, nodeFunc, nodeFunc);
    }

    /**
     * \brief Traverse tree and visit each leaf node
     *
     * The passed callback function is called with the
     * node and corresponding treepath as arguments.
     *
     * \param tree The tree to traverse
     * \param leafFunc This function is called for each leaf node
     */
    template<class Tree, class LeafFunc>
    void forEachLeafNode(Tree&& tree, LeafFunc&& leafFunc)
    {
      auto nop = [](auto&&... args) {};
      forEachNode(tree, nop, leafFunc, nop);
    }

    //! \} group Tree Traversal

  } // namespace TypeTree
} //namespace Dune

#endif // DUNE_TYPETREE_TRAVERSAL_HH
