import cmd
import ec
import getpass
import sys
from getopt import getopt, GetoptError

prog_name = "py3amulecmd"
prog_ver  = "0.1"

class REPL(cmd.Cmd):
    
    def __init__(self):
        
        self.host = b"localhost"
        self.port = 4712
        self.passwd = None

        self.prompt = "> "
        self.intro = "Welcome to %s %s" % (prog_name, prog_ver)
        self.ec = None
        
        if len(sys.argv) > 1:
            try:
                options, args = getopt(sys.argv[1:], 'vhs:p:w:', ["version", "help", "server=","port=","password="])

                for option, argument in options:
                    if option in ("-v", "--version"):
                        print (prog_name, prog_ver)
                        exit()
                    elif option in ("-h", "--help"):
                        self.print_help()
                        exit()
                    elif option in ("-s", "--server"):
                        self.host = argument.encode(encoding='utf_8', errors='strict')
                    elif option in ("-p", "--port"):
                        self.port = argument
                    elif option in ("-w", "--password"):
                        self.passwd = argument.encode(encoding='utf_8', errors='strict')

            except GetoptError:
                print ('Unknown Argument(s) "%s"'," ".join(sys.argv[1:]))
                self.print_help()
                exit()
                
        cmd.Cmd.__init__(self)
        
    def print_help(self):
            print ()
            print (prog_name,"v"+prog_ver)
            print ()
            if (sys.argv[0].endswith(".py")):
                print ("Usage: python",prog_name+".py","[options]")
            else:
                print ("Usage:",prog_name,"[options]")
            print ()
            print ("<Options>")
            print ("  -v, --version", " " * 20, "Print version to terminal")
            print ("  -s, --server=<server name or ip>", " " * 1, "Set domain name or ip of the aMule Server")
            print ("  -p, --port=<port number>", " " * 9, "Set port number of the server")
            print ("  -w, --password=<password>", " " * 8, "Set password the server")
            print ("  -h, --help", " " * 23, "Display this help screen")
            print ()
        
    def preloop(self):
        if self.passwd == None:
            self.passwd = getpass.getpass("Password: ").encode(encoding='utf_8', errors='strict')
        
        try:
            self.ec = ec.conn(self.passwd, self.host, self.port, prog_name, prog_ver)
        except ec.ConnectionFailedError:
            print("Connection failed")
            sys.exit()
    def do_quit(self, arg):
        sys.exit()
    def do_exit(self, arg):
        sys.exit()
    def do_EOF(self, arg):
        sys.exit()
    def do_connect(self, arg):
        self.ec.connect()
    def do_disconnect(self, arg):
        self.ec.disconnect()
    def do_status(self, arg):
        print (self.ec.get_status())
    def do_shutdown(self, arg):
        self.ec.shutdown()
        sys.exit()

def main():
    repl = REPL()
    repl.cmdloop()

if __name__ == "__main__":
    main()