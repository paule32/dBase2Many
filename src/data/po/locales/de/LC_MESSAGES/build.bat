msgfmt -o cc.mo cc.po
msgfmt -o lisp.mo lisp.po
msgfmt -o dbase.mo dbase.po
msgfmt -o pascal.mo pascal.po
msgfmt -o doxygen.mo doxygen.po
msgfmt -o runner.mo runner.po

pyrcc5 -o de_locales_rc.py de_locales.qrc
