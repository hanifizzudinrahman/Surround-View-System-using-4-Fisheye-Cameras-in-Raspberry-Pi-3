# Copy Images and Rename
import os
import glob

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
print(">"*50)
print()
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# Function to rename multiple files 
def main(): 
    a,b,c,d = 0,0,0,0
    print("==> Camera A-B-C-D")

    for filename in glob.glob("*.jpg"): 
        print('Before: ', filename)
        if filename[:9] == "Camera_A_":
            newFilename = "Camera_A_"
            a += 1
            newFilename = newFilename + str(a) + ".jpg"
        elif filename[:9] == "Camera_B_":
            newFilename = "Camera_B_"
            b += 1
            newFilename = newFilename + str(b) + ".jpg"
        elif filename[:9] == "Camera_C_":
            newFilename = "Camera_C_"
            c += 1
            newFilename = newFilename + str(c) + ".jpg"
        elif filename[:9] == "Camera_D_":
            newFilename = "Camera_D_"
            d += 1
            newFilename = newFilename + str(d) + ".jpg"
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