.list off
.ifndef JOB_DESC_INC
JOB_DESC_INC = 1

.global JobDesc, JobDescPtrs

.scope JobDesc

        Start := bank_start JobDesc

; ##############################################################################
; ###          AUTOMATICALLY GENERATED CODE, DO NOT MODIFY MANUALLY          ###
; ##############################################################################

        ARRAY_LENGTH = 22

        _0 := JobDesc + 0
        _1 := JobDesc + 30
        _2 := JobDesc + 62
        _3 := JobDesc + 103
        _4 := JobDesc + 139
        _5 := JobDesc + 179
        _6 := JobDesc + 223
        _7 := JobDesc + 265
        _8 := JobDesc + 297
        _9 := JobDesc + 327
        _10 := JobDesc + 357
        _11 := JobDesc + 388
        _12 := JobDesc + 420
        _13 := JobDesc + 462
        _14 := JobDesc + 499
        _15 := JobDesc + 544
        _16 := JobDesc + 580
        _17 := JobDesc + 622
        _18 := JobDesc + 658
        _19 := JobDesc + 696
        _20 := JobDesc + 735
        _21 := JobDesc + 781

; ##############################################################################

.endscope

.endif
.list on
