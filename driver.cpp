#include<stdio.h>
#include<cstdlib>
#include<vector>
#include<time.h>

using namespace std;

int main(){
	srand(time(0));
	int maxNodes = 10;
	int randNodes = rand(3, 10);

	//Finding the maximum amount of paths
	int temp = 0;
	for(int i = 0; i < randNodes; i++){
		temp += randNodes-1-i;
	}

	int randPaths = rand(randNodes-1, temp);
	int paths[randNodes][randNodes];

	//Development of paths between nodes
	int set;
	int count = 0;
	for(int i = 0; count < randPaths; i++){
		for(int j = 0; j < i; j++){
			set = rand(1,3);
			if((set == 1) && (path[i][j] == 0) && (i != j){
				path[i][j] = 1;
				count++;
			}
		}
		if(i == randNodes){
			i = 0;
		}
	}

	//Initializing the 2D vector
	vector<vector<int>> map;
	//Developing the Paths between Nodes
	while(randPaths != 0){
		
		randPaths--;
	}
}
