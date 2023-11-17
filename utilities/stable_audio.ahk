^j::

    ; Set the number of repetitions
    repetitions := 10
    CoordMode, Mouse, Screen

    ; Main Loop
    Loop, %repetitions%
    {
        ; Action 1: Select text box
        Click, 144, 309
        Sleep, 100 ; triple click
        Click, 144, 309
        Sleep, 100 
        Click, 144, 309
        Sleep, 500

        ; Action 2: Type Text
        Send, "ambient, comfort, meditation, low synths, twinkle, peaceful, warm soft hug" ; Prompt
        Sleep, 500
        Click, 597, 578

        ; Action 3: Waits for generation to complete
        Sleep, 48000

        ; Action 4: Download flow
        Click, 596, 699
        Sleep, 500
        Click, 1163, 708
        Sleep, 13000 ; Waits download to start

        ; Action 7: Closes download page
        Click, 1184, 381
        Sleep, 500
    }
