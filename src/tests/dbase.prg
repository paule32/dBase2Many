// ----------------------------------------------------------------------------
// \file  dbase.prg
// \note  (c) 2025, 2026 by Jens Kallup - paule32
//        all rights reserved.
// ----------------------------------------------------------------------------
#ifndef __DBASE_PRG__
#define __DBASE_PRG__

NOTE comment line

SET ESCAPE ON

SET FORMAT TO SCREEN
SET MARGIN TO 10pt, 10pt

#include "test.prg"         // test file include
#define name(x,y) #x + #y

ERASE

TEXT
// This is a C++ like one line comment
** This is a dBase comment line style A
&& This is a dBase comment line style B
ENDTEXT

/* This is a 
   multiline C like comment block
   /* you can nested it */
*/

WRITE name(Hello, World)
X = 23
WRITE X
X = X + 1
IF X == 22
    WRITE "X := " + X
ENDIF

INPUT "Test input: " TO memVar
IF memVar == "abc"
    INPUT memVar TO cc
    WRITE "no input"
ENDIF

IF 2 == (x + 1)
    WRITE "falsch"
ELSE
    IF 3 < 3
        WRITE "huch" + " hach" + 'xxxx'
    ELSE
        WRITE "sonst"
    ENDIF
    WRITE "naja"
    IF x == 23
        WRITE "2222"
    ENDIF
    X = X + 1
    IF X == 24
        WRITE "OKAY"
    ENDIF
ENDIF

PARAMETER bmodal
LOCAL B
B = NEW ParentForm(51,4)
B.Init(121,2)
B.Open()

CLASS ParentForm OF FORM
    PROPERTY width = 200.23
    PROPERTY top   = 231
    
    WITH (THIS)
        onClick = THIS.ParentForm_onClick   ** single handler
        Width = 400
        Height = 400
        Top = 223
        Left = 200
    ENDWITH

    // -----------------------------------------------------
    // \brief you can create properties with THIS.path ...
    // -----------------------------------------------------
    THIS.PushButton1 = NEW PUSHBUTTON(THIS)
    THIS.PushButton1.Top = 180
    THIS.PushButton1.Left = 30
    
    // -----------------------------------------------------
    // \brief or you can WITH to bundle properties from one
    //        object.
    // -----------------------------------------------------
    WITH (THIS.PushButton1)
        onClick = { THIS.PushButton1_onClick_1 ;  ** multiple handler call: 1
                    THIS.PushButton1_onClick_2 ;  ** multiple handler call: 2
                    THIS.PushButton1_onClick_3 }  ** multiple handler call: 3
                    
        onMouseMove     = THIS.PushButton1_onMouseMove
        onMouseRButton  = THIS.PushButton1_onMouseRButton
        
        Top = 82
        Width = 128
        Text = "Click Me"
    ENDWITH
    
    THIS.PushButton2 = NEW PUSHBUTTON(THIS)
    WITH (THIS.PushButton2)
        onClick = THIS.PushButton2_onClick
        Font = NEW FONT("Arial",12, .T., .T., .T.)
        Font.bold = .F.
        Left = 200
        Top = 82
        Width = 128
        Text = "Click Me, too"
    ENDWITH

    THIS.Container1 = NEW CONTAINER(THIS)
    WITH (THIS.Container1)
        Left = 20
        Top = 190
        Width = 300
        Height = 180
        BackColor = "#202225"
        BorderColor = "#7a1c1c"
        BorderWidth = 2
        Radius = 10
    ENDWITH

    THIS.Container1.PushButton1 = NEW PUSHBUTTON(THIS.Container1)
    WITH (THIS.Container1.PushButton1)
        Left = 20
        Top = 20
        Width = 120
        Height = 28
        Text = "OK"
    ENDWITH

    THIS.Container1.ComboBox1 = NEW COMBOBOX(THIS.Container1)
    WITH (THIS.Container1.ComboBox1)
        Left = 150
        Top = 20
        Width = 120
        Height = 28
        Items = "Apfel,Birne,Bananne"
    ENDWITH
    
    WRITE "===> " + THIS.width
    METHOD Init(a,c)        
        WRITE "ParentForm.Init()"
        WRITE (a + 10)
        WRITE (a + 2)
        WRITE this.PushButton1
        I = 1
        E = 42
        FOR I = 1 TO 3
            WRITE "I = " + I
            E = E + 1
            WRITE E
            WRITE "x= " + THIS.TestProc(THIS, "text 1")
            WRITE "--> " + THIS.Width + " okay."
            IF I == 3 RETURN ENDIF
            BREAK
        ENDFOR
        WRITE "go along"
    ENDMETHOD
    
    METHOD TestProc(Sender)
        WRITE Sender
        RETURN 324
    ENDMETHOD
    
    METHOD testProcer()
        WRITE "test procer"
        INPUT "Test input: " TO THIS.memVar
        IF THIS.memVar == "abc"
            INPUT THIS.memVar TO cc
            WRITE "no input: " + cc
        ENDIF
    ENDMETHOD

    // --------------------------------------------------------------
    // \brief This is a onClick Event methode. It will be execute
    //        when you mouse click in the child-area of window/form.
    // --------------------------------------------------------------
    METHOD ParentForm_onClick(Sender)
        WRITE "on form clicked"
        v = 43
        a = 15
        DO CASE
            CASE v == 40 WRITE "-32-"
            CASE v == 41 WRITE "-42-"
            OTHERWISE
                DO CASE
                    CASE a == 15
                        WRITE "OK"
                        DO THIS.testProcer()
                        DO test
                ENDCASE
                WRITE "fallback"
                WRITE "other"
        ENDCASE
        x = 5
        WRITE X
        DO WHILE x >= 2
            WRITE x
            x = x - 1
            IF x == 3
                BREAK
            ENDIf
        ENDDO
        WRITE "----->"
        // CREATE FILE "33.txt"
    ENDMETHOD
    
    // --------------------------------------------------------------
    // \brief This is a onClick Event methode. It will be execute
    //        when you mouse click the left button on the form.
    // --------------------------------------------------------------
    METHOD PushButton1_onClick_1(Sender)
        THIS.Width = THIS.Width + 10
        WRITE "clicked button A: handler 1"
        WRITE Sender.Text
        WITH (Sender)           ** you can have nested WITH
            WRITE Text
            WITH (Font)         ** ENDWITH blocks
                bold = .T.
                size = 14
            ENDWITH
        ENDWITH
        IF THIS.PushButton1.Text == "Click Me"
            THIS.PushButton2.Text = "Click Me"
            WRITE "okk"
            WITH (Sender)
                Text = "Click Me, too"
            ENDWITH
        ELSE
            THIS.PushButton2.Text = "Click Me, too"
            Sender.Text = "Click Me"
            Sender.Font.bold = .F.
            Sender.Font.Size = 11
        ENDIF
    ENDMETHOD
    METHOD PushButton1_onClick_2(Sender)
        WRITE "clicked button A: handler 2"
    ENDMETHOD
    METHOD PushButton1_onClick_3(Sender)
        WRITE "clicked button A: handler 3"
    ENDMETHOD
    METHOD PushButton1_onMouseRButton(Sender)
        WRITE "right click"
    ENDMETHOD
    
    METHOD PushButton1_onMouseMove(Sender)
        WRITE [over button: 1 " ]
    ENDMETHOD
    
    METHOD PushButton2_onClick(Sender)
        WRITE "clicked button 2"
        WRITE Sender.Text
        IF THIS.PushButton2.Text == "Click Me, too"
            THIS.PushButton1.Text = "Click Me"
            Sender.Text = "Click Me"
        ELSE
            THIS.PushButton1.Text = "Click Me"
            Sender.Text = "Click Me, too"
        ENDIF
    ENDMETHOD
ENDCLASS


CLASS Form1 OF ParentForm
    THIS.PushButton1 = NEW PUSHBUTTON(THIS)
    
    METHOD Init(a,b,c,d,e,F)
        CALL SUPER::Init(B)
        WRITE "Hallo " + F / 3
        WRITE A
        FOR I = 1 TO 3
            WRITE "I = " + I
            E = E + 1
            WRITE E
        ENDFOR
    ENDMETHOD
ENDCLASS

CLASS Form2 OF FORM1
ENDCLASS

// CALL Form1.Init("Ooops",2,3,4,5,6)
#endif  // __DBASE_PRG__