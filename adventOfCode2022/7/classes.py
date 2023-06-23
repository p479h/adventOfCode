class File:
    def __init__(self, name: str, size: int, parent: "Directory") -> "File":
        self.name = name
        self.size = size
        self.parent = parent

    def __repr__(self) -> str:
        return "%s (file, size=%i)" % (self.name, self.size)


class Directory:
    def __init__(self, name: str, parent: "Directory" = None) -> "Directory":
        self.name = name
        self.parent = parent
        self.children = {}
        self.size = None

    def process_command(self, command: str) -> None:
        if command.startswith("$ ls"):
            self.process_ls(command)
            return self
        elif command.startswith("$ cd"):
            directory = self.process_cd(command)
            return directory
        else:
            print("Command not recognized")

    def process_ls(self, command: str) -> None:
        for line in command.split("\n"):
            if line.startswith("$"): #Command itself
                continue
            if line.startswith("dir"):
                dirname = line.replace("dir ", "")
                if not dirname in self.children:
                    self.make_child_dir(dirname)
            else: # file
                size, filename = line.split(" ")
                if filename not in self.children:
                    self.make_child_file(filename, int(size))

    def process_cd(self, command: str) -> "Directory":
        dirname = command.replace("$ cd ", "")
        if dirname == "..":
            return self.parent
        elif dirname in self.children:
            return self.children[dirname]
    
    def make_child_dir(self, name: str) -> "Directory":
        child = self.make_dir(name, parent = self)
        self.children[name] = child
        return child

    def make_child_file(self, name: str, size: int) -> "File":
        file = File(name, size, parent = self)
        self.children[name] = file
        return file

    def __repr__(self) -> str:
        if self.size is None:
            return "%s (dir)" % self.name
        return "%s (dir, SIZE=%i)" % (self.name, self.size)
    
    def tree(self, count: int = 0):
        #Printing own directory
        if count:
            print("\t"*count, end = "")
        print(self)
        
        #Printing child files, then directories
        count = count + 1
        later = {}
        for name, child in self.children.items():
            if type(child) == type(self):
                later[name] = child
            else:
                print("\t"*count, child, sep = "")
                
        for name, directory in later.items():
            directory.tree(count)

    @classmethod
    def make_dir(cls, name: str, parent: "Directory"):
        return cls(name, parent)

    def compute_size(self) -> int:
        total_size = 0
        for name, child in self.children.items():
            if type(child) == type(self):
                total_size += child.compute_size()
            else:
                total_size += child.size #FILE!!!
        self.size = total_size
        return total_size

    def find_sum_under(self, thresshold: int) -> int:
        if self.size is None:
            self.compute_size()

        amount_children = 0
        for child in self.children.values():
            if type(child) == type(self):
                if child.size > thresshold:
                    amount_children += child.find_sum_under(thresshold)
                else:
                    amount_children += child.size
        return amount_children

    def find_dirs_under(self, thress: int, dirs: list = None) -> list:
        if self.size is None:
            self.compute_size()
            
        if dirs is None:
            dirs = []

        for child in self.children.values():
            if not (type(child) == type(self)):
                continue
            if child.size < thress:
                dirs.append(child)
            child.find_dirs_under(thress, dirs)

        return dirs

    def find_dirs_over(self, thress: int, dirs: list = None) -> list:
        if self.size is None:
            self.compute_size()
            
        if dirs is None:
            dirs = []

        for child in self.children.values():
            if not (type(child) == type(self)):
                continue
            if child.size > thress:
                dirs.append(child)
                child.find_dirs_over(thress, dirs)
        return dirs
