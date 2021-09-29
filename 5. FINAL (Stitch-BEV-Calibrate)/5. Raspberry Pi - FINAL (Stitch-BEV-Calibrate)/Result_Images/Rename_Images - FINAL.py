# Copy Images and Rename
import os
import glob

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print(">"*50)
print()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Function to rename multiple files 
def main(): 
    i,j = 0,0
    print("==> Stitching")

    for filename in glob.glob("*.jpg"): 
        print('Before: ', filename)
        if filename[:12] == "FINAL (FPS) ":
            newFilename = filename[:12]
            i += 1
            newFilename = newFilename + str(i) + ".jpg"
        else:
            newFilename = filename[:6]
            j += 1
            newFilename = newFilename + str(j) + ".jpg"
        print("=> ", newFilename)
        # rename all the files 
        os.rename(filename, newFilename)
  
# Driver Code 
if __name__ == '__main__':       
    # Calling main() function 
    main()

    # Click Enter
    print('Click Enter!')
    x = input()
