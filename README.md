# MLInference-Chih-Che_Fang
The source code owned by me, I don't share this source with anyone  
Please grade groupwork individually  

# How to Run the Program  
1.	Change to the root directory of this project  
2.	Execute run_test.bat, it will automatically run the docker image and perform a http request to the server with image files. Explanation for the command executed:
	Run docker image: docker run -d -p 5000:5000 myimage 
	Request inference: curl -X POST -F file=@dog1.jpg -F file=@dog2.jpg -F file=@cat1.jpg -F file=@cat2.jpg -F file=@squirrel1.jpg http://localhost:5000/predict 
3.	See the classification results of all images on consle (This server support multiple images in one single http request).  