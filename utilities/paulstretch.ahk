^p::

    ; Set the number of repetitions
    repetitions := 24
    CoordMode, Mouse, Screen

    ; Main Loop
    Loop, %repetitions%
    {
        MouseClickDrag, Left, 1230, 291, 335, 861
        Sleep, 500

        ; Action 4: Download flow
        Click, 397, 65
        Sleep, 500
        Click, 597, 341
        Sleep, 15000 ; Waits download to start

        MouseClickDrag, Left, 1230, 291, 1204, 257
        Sleep, 500
    }
