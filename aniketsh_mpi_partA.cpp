#include "mpi.h"
#include <algorithm>
#include <cstdlib>
#include <cctype>
#include <cmath>
#include <sstream>
#include <fstream>
#include <iostream>
#include <vector>



/************* Feel free to change code below (even main() function), add functions, etc.. But do not change CL arguments *************/
int* prewitt(int *inputImage, int height_org, int width, int numProcesses){
  int maskX[3][3];
  int maskY[3][3];
  int grad_x;
  int grad_y;
  int grad;
  int height = height_org / numProcesses;
  int* outputImage = (int*)malloc(sizeof(int)*(height*width));

  printf("My height is %d\n",height);

  maskX[0][0] = +1; maskX[0][1] = 0; maskX[0][2] = -1;

  maskX[1][0] = +1; maskX[1][1] = 0; maskX[1][2] = -1;

  maskX[2][0] = +1; maskX[2][1] = 0; maskX[2][2] = -1;

  maskY[0][0] = +1; maskY[0][1] = +1; maskY[0][2] = +1;
  
  maskY[1][0] =   0; maskY[1][1] =   0; maskY[1][2] =    0;

  maskY[2][0] =  -1; maskY[2][1] =  -1; maskY[2][2] =  -1;

  for( int x = 0; x < height; ++x ){

    for( int y = 0; y < width;  ++y ){

      grad_x = 0;

      grad_y = 0;

    /* For handling image boundaries */

      if( x == 0 || x == (height-1) || y == 0 || y == (width-1))

	grad = 0;

      else{

      /* Gradient calculation in X Dimension */
	int i;
	int j;
      for( int i = -1; i <= 1; i++ )  {

	for( int j = -1; j <= 1; j++ ){

	  grad_x += (inputImage[((x+i)*width)+(y+j)] * maskX[i+1][j+1]);

	}

      }

      /* Gradient calculation in Y Dimension */

      for(i=-1; i<=1; i++)  {

	for(j=-1; j<=1; j++){

	  grad_y += (inputImage[((x+i)*width)+(y+j)] * maskY[i+1][j+1]);

	}

      }

      /* Gradient magnitude */

      grad = (int) sqrt( (grad_x * grad_x) + (grad_y * grad_y) );

    }

      if (grad < 0){
        grad = 0;
      }
      if (grad > 255){
        grad = 255;
      }
      outputImage[(x*width)+y] = grad;

  }

 }

  return outputImage;
}


int* processImage(int sizeincoming){
  int *k = (int*)malloc(sizeof(int)*sizeincoming);
  for (int i = 0; i < sizeincoming;i++){
    k[i] = 250;
  }
  return k;
}

int main(int argc, char* argv[])
{
	int processId, num_processes, image_height, image_width, image_maxShades;
	int *inputImage, *outputImage;
	
	// Setup MPI
    MPI_Init( &argc, &argv );
    MPI_Comm_rank( MPI_COMM_WORLD, &processId);
    MPI_Comm_size( MPI_COMM_WORLD, &num_processes);
	
    if(argc != 3)
    {
		if(processId == 0)
			std::cout << "ERROR: Incorrect number of arguments. Format is: <Input image filename> <Output image filename>" << std::endl;
		MPI_Finalize();
        return 0;
    }
	
	if(processId == 0)
	{
		std::ifstream file(argv[1]);
		if(!file.is_open())
		{
			std::cout << "ERROR: Could not open file " << argv[1] << std::endl;
			MPI_Finalize();
			return 0;
		}

		std::cout << "Detect edges in " << argv[1] << " using " << num_processes << " processes\n" << std::endl;

		std::string workString;
		/* Remove comments '#' and check image format */ 
		while(std::getline(file,workString))
		{
			if( workString.at(0) != '#' ){
				if( workString.at(1) != '2' ){
					std::cout << "Input image is not a valid PGM image" << std::endl;
					return 0;
				} else {
					break;
				}       
			} else {
				continue;
			}
		}
		/* Check image size */ 
		while(std::getline(file,workString))
		{
			if( workString.at(0) != '#' ){
				std::stringstream stream(workString);
				int n;
				stream >> n;
				image_width = n;
				stream >> n;
				image_height = n;
				break;
			} else {
				continue;
			}
		}
		inputImage  = new int[image_height*image_width];

		/* Check image max shades */ 
		while(std::getline(file,workString))
		{
			if( workString.at(0) != '#' ){
				std::stringstream stream(workString);
				stream >> image_maxShades;
				break;
			} else {
				continue;
			}
		}
		/* Fill input image matrix */ 
		int pixel_val;
		for( int i = 0; i < image_height; i++ )
		{
			if( std::getline(file,workString) && workString.at(0) != '#' ){
				std::stringstream stream(workString);
				for( int j = 0; j < image_width; j++ ){
					if( !stream )
						break;
					stream >> pixel_val;
					inputImage[(i*image_width)+j] = pixel_val;
				}
			} else {
				continue;
			}
		}
		outputImage = (int*)malloc(sizeof(int)*image_width*image_height);
	   
	} // Done with reading image using process 0
	MPI_Bcast(&image_height, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&image_width, 1, MPI_INT, 0, MPI_COMM_WORLD);
	int elements_per_proc = (image_height * image_width)/num_processes;
	
	printf("The elements per proc is %d  %d\n", image_height, image_width);
        int *sub_in = (int*)malloc(sizeof(int)*elements_per_proc);
	MPI_Scatter(inputImage, elements_per_proc, MPI_INT, sub_in, elements_per_proc, MPI_INT, 0, MPI_COMM_WORLD);
        int* other_sub_in = prewitt(sub_in, image_height,image_width,num_processes); 
        MPI_Gather(other_sub_in, elements_per_proc, MPI_INT, outputImage, elements_per_proc, MPI_INT, 0,MPI_COMM_WORLD);
	if(processId == 0)
	{
		/* Start writing output to your file */
		std::ofstream ofile(argv[2]);
		if( ofile.is_open() )
		{
			ofile << "P2" << "\n" << image_width << " " << image_height << "\n" << image_maxShades << "\n";
			for( int i = 0; i < image_height; i++ )
			{
				for( int j = 0; j < image_width; j++ ){
				  ofile << outputImage[(i*image_width)+j] << " ";
				}
				ofile << "\n";
			}
		} else {
			std::cout << "ERROR: Could not open output file " << argv[2] << std::endl;
			return 0;
		}
	 }
	 
    MPI_Finalize();
    return 0;
}
