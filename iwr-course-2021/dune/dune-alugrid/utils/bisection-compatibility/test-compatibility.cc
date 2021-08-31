#include "bisectioncompatibility.hh"
#include <iostream>

int main()
{
  typedef BisectionCompatibility::ElementType ElementType;

  std::vector<ElementType> elements(
    {
      {10,13,27,28},
      {13,1,10,27},
      {10,9,13,28},
      {13,27,28,29},
      {1,13,10,31},
      {4,1,13,27},
      {9,10,13,40},
      {13,9,12,28},
      {13,4,27,29},
      {12,13,28,29},
      {27,0,28,29},
      {1,4,13,31},
      {13,10,31,32},
      {9,13,12,40},
      {13,10,39,40},
      {13,3,4,29},
      {12,3,13,29},
      {13,4,30,31},
      {14,10,13,32},
      {30,13,31,32},
      {13,12,40,41},
      {13,10,22,39},
      {39,13,40,41},
      {3,13,4,34},
      {3,12,13,34},
      {13,4,14,30},
      {10,14,13,42},
      {11,10,14,32},
      {14,13,30,32},
      {2,30,31,32},
      {22,12,13,41},
      {10,13,22,44},
      {22,13,39,41},
      {22,10,19,39},
      {18,39,40,41},
      {4,13,33,34},
      {12,13,34,35},
      {4,13,14,36},
      {14,4,5,30},
      {10,11,14,42},
      {13,10,42,44},
      {14,13,42,43},
      {12,22,13,47},
      {21,12,22,41},
      {10,22,19,44},
      {22,13,43,44},
      {16,4,13,33},
      {13,33,34,35},
      {13,12,16,35},
      {4,13,36,38},
      {4,14,5,36},
      {13,14,36,37},
      {13,42,43,44},
      {23,13,14,43},
      {12,21,22,47},
      {12,13,45,47},
      {13,22,46,47},
      {22,13,23,43},
      {4,16,13,38},
      {7,4,16,33},
      {13,16,33,35},
      {33,6,34,35},
      {12,13,16,45},
      {16,12,15,35},
      {36,13,37,38},
      {14,13,17,37},
      {42,20,43,44},
      {13,23,14,49},
      {45,13,46,47},
      {25,13,22,46},
      {13,22,23,49},
      {4,7,16,38},
      {13,16,37,38},
      {12,16,15,45},
      {13,16,45,46},
      {8,36,37,38},
      {13,14,17,48},
      {17,13,16,37},
      {13,14,48,49},
      {24,45,46,47},
      {13,25,22,50},
      {16,13,25,46},
      {13,22,49,50},
      {13,17,16,48},
      {48,13,49,50},
      {13,16,25,50},
      {16,13,48,50},
      {26,48,49,50}
    });

 /* std::vector<ElementType> elements(
  {
    {0,1,2,3},
    {3,0,1,4},
    {4,1,0,5},
    {1,2,0,5}
  });*/

  BisectionCompatibility bisComp(elements, false);
  std::cout << "Construction worked" << std::endl;
  if(bisComp.compatibilityCheck())
    std::cout << "Refinement is okay" << std::endl;
  else
  if(bisComp.type0Algorithm() )
    std::cout << "DONE" << std::endl;
  else
    std::cout << "COULD NOT MAKE COMPATIBLE!" << std::endl;

  if(bisComp.compatibilityCheck())
    std::cout << "Refinement is okay" << std::endl;
  else
  if(bisComp.type1Algorithm() )
    std::cout << "DONE" << std::endl;
  else
   std::cout << "COULD NOT MAKE COMPATIBLE!" << std::endl;

  // bisComp.printNB();
  for(unsigned int i=0; i < elements.size(); ++i)
  {
    std::cout << i << ": ";
    bisComp.printElement(i);
  }

  return 0;
}