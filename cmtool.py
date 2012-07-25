from riobus import RioBus

if __name__ == "__main__":
    from coopy.base import init_persistent_system
    riobus = init_persistent_system(RioBus())

    while True:
        print('''
                (l) lista as linhas\n
                (t) total de linhas\n
                (s) total de linhas\n
                (q) sair\n
              ''')

        c = raw_input("             >> ")
        if c == "q":
            break
        elif c == "l":
            for name, line in riobus.lines.items():
                print("Linha %s\n Ruas:\n%s\n" % (name,
                                                 str(line)))
        elif c == "s":
            valor = raw_input("           >>")
            for k, item in riobus.search_street(valor).items():
                print(item)
        elif c == "t":
            print('%s total de linhas' % (len(riobus.lines)))

