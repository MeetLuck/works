import cmd
class Hello(cmd.Cmd):
    ''' Simple command processor'''
    def do_greet(self,person):
        """greet [person]
        Greet the named person"""
        if person:
            print 'hello', person
        else:
            print 'hi'
    def help_greet(self):
        print '\n'.join( ['greet [person]', 'Greet the named person'] )
    def do_EOF(self,line):
        return True

if __name__ == '__main__':
    Hello().cmdloop()
