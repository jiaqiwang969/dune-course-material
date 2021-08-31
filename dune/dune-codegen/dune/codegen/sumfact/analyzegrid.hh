#ifndef DUNE_CODEGEN_SUMFACT_ANALYZEGRID_HH
#define DUNE_CODEGEN_SUMFACT_ANALYZEGRID_HH

#include<fstream>
#include<set>
#include<string>

#include <dune/pdelab/common/intersectiontype.hh>


struct GridInfo{
  int dim;
  int number_of_elements;
  int number_of_skeleton_faces;
  int number_of_boundary_faces;
  std::set<std::size_t> skeleton_variants;
  std::set<std::size_t> boundary_variants;

  void export_grid_info(std::string);

  friend std::ostream & operator<<(std::ostream &os, const GridInfo& grid_info);
};

void GridInfo::export_grid_info(std::string filename){
  std::ofstream output_file;
  output_file.open(filename);
  for (std::size_t var : skeleton_variants){
    std::size_t index_s = var / (2 * dim);
    std::size_t facedir_s = index_s / 2;
    std::size_t facemod_s = index_s % 2;

    std::size_t index_n = var % (2 * dim);
    std::size_t facedir_n = index_n / 2;
    std::size_t facemod_n = index_n % 2;

    output_file << "skeleton" << " "
                << facedir_s << " "
                << facemod_s << " "
                << facedir_n << " "
                << facemod_n << std::endl;
  }
  for (std::size_t var : boundary_variants){
    std::size_t index_s = var;
    std::size_t facedir_s = index_s / 2;
    std::size_t facemod_s = index_s % 2;

    output_file << "boundary" << " "
                << facedir_s << " "
                << facemod_s << " "
                << -1 << " "
                << -1 << std::endl;
  }
  output_file.close();
}

std::ostream & operator<<(std::ostream &os, const GridInfo& grid_info){
  return os << "== Print GridInfo" << std::endl
            << "Dimension: " << grid_info.dim << std::endl
            << "Number of elements: " << grid_info.number_of_elements << std::endl
            << std::endl
            << "Number of skeleton faces: " << grid_info.number_of_skeleton_faces << std::endl
            << "Number of skeleton variants: " << grid_info.skeleton_variants.size() << std::endl
            << std::endl
            << "Number of boundary faces: " << grid_info.number_of_boundary_faces << std::endl
            << "Number of boundary variants: " << grid_info.boundary_variants.size() << std::endl;
}


template <typename ES>
void analyze_grid(const ES& es, std::string filename){
  const int dim = ES::dimension;

  GridInfo grid_info;
  grid_info.dim = dim;
  grid_info.number_of_elements = 0;
  grid_info.number_of_skeleton_faces = 0;
  grid_info.number_of_boundary_faces = 0;


  auto& index_set = es.indexSet();
  for (const auto& element : elements(es)){
    grid_info.number_of_elements += 1;

    auto ids = index_set.index(element);

    for (const auto& intersection : intersections(es, element)){
      auto intersection_data = Dune::PDELab::classifyIntersection(es, intersection);
      auto intersection_type = std::get<0>(intersection_data);
      auto& outside_element = std::get<1>(intersection_data);

      switch(intersection_type){
      case Dune::PDELab::IntersectionType::skeleton :
      {
        auto idn = index_set.index(outside_element);
        bool first_visit = ids > idn;
        if (first_visit){
          grid_info.number_of_skeleton_faces += 1;

          size_t facedir_s = intersection.indexInInside() / 2 ;
          size_t facemod_s = intersection.indexInInside() % 2 ;
          size_t facedir_n = intersection.indexInOutside() / 2 ;
          size_t facemod_n = intersection.indexInOutside() % 2 ;

          // std::cout << facedir_s << " "
          //           << facemod_s << " "
          //           << facedir_n << " "
          //           << facemod_n << std::endl;

          size_t variant = intersection.indexInOutside() + 2 * dim * intersection.indexInInside();
          grid_info.skeleton_variants.insert(variant);
        }

        break;
      }
      case Dune::PDELab::IntersectionType::periodic :
      {
        assert (false);
        break;
      }
      case Dune::PDELab::IntersectionType::boundary :
      {
        grid_info.number_of_boundary_faces += 1;

        size_t variant = intersection.indexInInside();
        grid_info.boundary_variants.insert(variant);

        break;
      }
      case Dune::PDELab::IntersectionType::processor :
      {
        assert (false);
        break;
      }
      }
    }
  }

  grid_info.export_grid_info(filename);
  std::cout << grid_info << std::endl;
}

#endif
