import os
try:
    import sass
except ImportError:
    print("FATAL: libsass not installed but required")
    exit(1)

proxmoxLibLocation = "/usr/share/javascript/proxmox-widget-toolkit/proxmoxlib.js"

def appendThemeMap(themeFileName, themeTitle):
    #open the proxmoxlib.js file
    f = open(proxmoxLibLocation, "r+", encoding="utf8")
    #read the file
    fileContents = f.read()

    #find the line that contains the theme_map variable
    themeMapLine = fileContents.find("theme_map: {")
    #find the end of the theme_map variable
    themeMapEnd = fileContents.find("}", themeMapLine)
    #get the theme_map variable
    themeMap = fileContents[themeMapLine:themeMapEnd]

    themeMap += "\"" + themeFileName + "\": \"" + themeTitle + "\",\n"

    #replace the theme_map variable with the new one
    fileContents = fileContents.replace(fileContents[themeMapLine:themeMapEnd], themeMap)

    #write to the file
    f.seek(0)
    f.write(fileContents)
    f.truncate()
    f.close()

def reinstallProxmoxWidgetToolkit():
    #if on linux, we should be on a proxmox machine, so apt reinstall proxmox-widget-toolkit to get the original proxmoxlib.js file
    if os.name == "posix":
        print("Reinstalling proxmox-widget-toolkit...")
        print("----------APT OUTPUT----------")
        os.system("apt -qq -o=Dpkg::Use-Pty=0 reinstall proxmox-widget-toolkit")
        print("------------------------------")

def compileSassThemes():
    print("Compiling SASS themes...")
    #get all of the .sass themes to compile
    themes = os.listdir("themes")

    for theme in themes:
        #check if it is a .sass file
        if theme.find(".sass") == -1:
            continue
        
        print("Compiling " + theme + "...")
        f = open("themes/" + theme, "r", encoding="utf8")
        #compile the sass file
        compiledSASS = sass.compile(string=f.read(), output_style="compressed")
        f.close()

        #create a new .css file with the compiled sass
        f = open("themes/" + theme[:theme.find(".sass")] + ".css", "w", encoding="utf8")
        f.write(compiledSASS)
        f.close()
    print("Done compiling SASS themes...")

#patches all of the themes into the proxmoxlib.js file and copys the themes into the themes folder
def patchThemes():
    print("Patching themes into proxmoxlib.js...")
    #get all of the .css themes to install in the themes folder
    themes = os.listdir("themes")

    for theme in themes:
        #check if it is a .css file
        if theme.find(".css") == -1:
            continue


        #read in the first line of the theme file
        f = open("themes/" + theme, "r", encoding="utf8")
        firstLine = f.readline()

        #extract the theme name from the first line comment, which is between /* and */
        themeTitle = firstLine[firstLine.find("/*!") + 3:firstLine.find("*/")]

        #get the theme file name without the .css extension and missing the theme- prefix
        themeFileName = theme[theme.find("theme-") + 6:theme.find(".css")]

        print("Patching " + themeTitle + " into proxmoxlib.js...")
        appendThemeMap(themeFileName, themeTitle)

    if os.name == "posix":
        #copy all the themes into the themes folder
        os.system("cp themes/* /usr/share/javascript/proxmox-widget-toolkit/themes")
    
    print("Done patching themes into proxmoxlib.js...")

def install():
    compileSassThemes()
    reinstallProxmoxWidgetToolkit()
    patchThemes()
    print("Done! Clear your browser cache and refresh the page to see the new themes.")

def uninstall():
    reinstallProxmoxWidgetToolkit()
    print("Custom themes uninstalled.")

def update():
    #git pull self
    os.system("git pull --quiet")
    #exit and run self
    os.system("python3 patch.py")

def main():
    print("PVEThemes Installer")
    print("By: Happyrobot33")
    print("Select an option:")
    print("-------------------")
    print("0. Exit")
    print("1. uninstall")
    print("2. install")
    print("3. update")
    print("4. compile sass themes")
    print("-------------------")
    choice = input("Enter a number: ")

    if choice == "0":
        exit()
    elif choice == "1":
        uninstall()
    elif choice == "2":
        install()
    elif choice == "3":
        update()
    elif choice == "4":
        compileSassThemes()
    else:
        print("Invalid choice")
        main()

if __name__ == "__main__":
    main()
