' statement for debugging: MsgBox "Entered value is " & Hide

Sub expand_columns_and_copy_data_to_clipboard()
    ' This function unhides all columns and then copies all rows and columns of data without the header to clipboard

    Call show_Diagnosis
    Call show_Reason_For_Exclusion
    Call show_Processing_Info
    Call show_Sorting_Info
    Call show_Flow_Sorting_Info
    Call show_Sequencing_Info
    Call show_scRNA_Sequencing_Info
    Call show_PPBC_Info
    Call show_WGS_Bulk_Info
    Call show_Curls_Info
    Call show_Microdissection_Info
    'Call show_Extraction_Info
    'Call show_WGS_Bulk_Sequencing_Info
    Call show_IF_Info
    Call show_Storage_Population
    Call show_DLP_Sequencing_Info
    Call show_MSK_DLP_Sequencing_Info
    Call show_BCCRC_DLP_Sequencing_Info

    Dim LastCell As String
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastCell = Last(3, rng)

    ' Select from A1 till the last cell in Rng
    With rng.Parent
        .Select
        .Range("A6", LastCell).Copy  ' A6 is top left data cell
    End With

End Sub

Sub shrink_columns()
    ' Shrink columns to hide fields that are not required

    Call show_hide_Diagnosis
    Call show_hide_Reason_For_exclusion
    Call show_hide_Processing_Info
    Call show_hide_Sorting_Info
    Call show_hide_Flow_Sorting_Info
    Call show_hide_Sequencing_Info
    Call show_hide_scRNA_Sequencing_Info
    Call show_hide_PPBC_Info
    Call show_hide_WGS_Bulk_Info
    Call show_hide_Curls_Info
    Call show_hide_Microdissection_Info
    'Call show_hide_Extraction_Info
    'Call show_hide_WGS_Bulk_Sequencing_Info
    Call show_hide_IF_Info
    Call show_hide_Storage_Population
    Call show_hide_DLP_Sequencing_Info
    Call show_hide_MSK_DLP_Sequencing_Info
    Call show_hide_BCCRC_DLP_Sequencing_Info

End Sub

Private Sub Worksheet_Change(ByVal Target As Range)
    ' Event handler for cell value change. Triggered when the value of a cell is changed.

    Dim LastCell As String
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastCell = Last(3, rng)

    If Not Intersect(Target, Me.Range("M6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Diagnosis
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("L6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Reason_For_exclusion
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("T6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Processing_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("Y6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Sorting_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("Z6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Flow_Sorting_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("Y6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Sequencing_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AE6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_scRNA_Sequencing_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("T6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_PPBC_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AT6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_WGS_Bulk_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AW6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Curls_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AW6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Microdissection_Info
        Application.EnableEvents = True
    End If

   'If Not Intersect(Target, Me.Range("AX6", LastCell)) Is Nothing Then
   '     Application.EnableEvents = False
   '     Call show_hide_Extraction_Info
   '     Application.EnableEvents = True
   ' End If

   'If Not Intersect(Target, Me.Range("AX6", LastCell)) Is Nothing Then
   '     Application.EnableEvents = False
   '     Call show_hide_WGS_Bulk_Sequencing_Info
   '     Application.EnableEvents = True
   ' End If

    If Not Intersect(Target, Me.Range("AT6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_IF_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("Y6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_Storage_Population
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AE6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_DLP_Sequencing_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AE6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_MSK_DLP_Sequencing_Info
        Application.EnableEvents = True
    End If

    If Not Intersect(Target, Me.Range("AE6", LastCell)) Is Nothing Then
        Application.EnableEvents = False
        Call show_hide_BCCRC_DLP_Sequencing_Info
        Application.EnableEvents = True
    End If

End Sub


' ######### show_hide and show functions START ################

Sub show_hide_Diagnosis()
    ' Show or hide columns based on "Final Pathology is Other"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Final Pathology")

    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Other" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Specify Diagnosis")

    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Diagnosis()
    ' show diagnosis

    colNum = ColumnNumber("Specify Diagnosis")
    Columns(colNum).EntireColumn.Hidden = False
End Sub


Sub show_hide_Reason_For_exclusion()
    ' Show or hide columns based on "Excluded is yes"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Excluded")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Yes" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Reason for Exclusion")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
    End If

End Sub

Sub show_Reason_For_Exclusion()
    ' show Reason For Exclusion

    colNum = ColumnNumber("Reason for Exclusion")
    Columns(colNum).EntireColumn.Hidden = False
End Sub

Sub show_hide_Processing_Info()
    ' Show or hide columns based on "Tissue Type is Single Cell Suspension"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Tissue Type")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Single Cell Suspension" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Total Cell Count (cells/ml)")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
        Columns(colNum + 3).EntireColumn.Hidden = True
        Columns(colNum + 4).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
    End If

End Sub

Sub show_Processing_Info()
    ' show Processing Info

    colNum = ColumnNumber("Total Cell Count (cells/ml)")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
    Columns(colNum + 3).EntireColumn.Hidden = False
    Columns(colNum + 4).EntireColumn.Hidden = False
End Sub


Sub show_hide_Sorting_Info()
    ' Show or hide columns based on "Downstream Submission is Sorted Single Cell Sequencing"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Downstream Submission")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Sorted Single Cell Sequencing" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Sorting Method")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Sorting_Info()
    ' show Sorting Info

    colNum = ColumnNumber("Sorting Method")
    Columns(colNum).EntireColumn.Hidden = False
End Sub

Sub show_hide_Flow_Sorting_Info()
    ' Show or hide columns based on "Sorting Method is Flow Sorting"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Sorting Method")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Flow Sorting" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Flow Instrument")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Flow_Sorting_Info()
    ' show Sorting Info

    colNum = ColumnNumber("Flow Instrument")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
End Sub


Sub show_hide_Sequencing_Info()
    ' Show or hide columns based on "Downstream Submission is Unsorted Single Cell Sequencing, Downstream Submission is Sorted Single Cell Sequencing"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Downstream Submission")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Unsorted Single Cell Sequencing" Or Cells(ii, triggerColNum).Value = "Sorted Single Cell Sequencing" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Submitted Populations")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Sequencing_Info()
    ' show Sequencing Info

    colNum = ColumnNumber("Submitted Populations")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
End Sub


Sub show_hide_scRNA_Sequencing_Info()
    ' Show or hide columns based on "Sequencing Technique is scRNA Sequencing"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Sequencing Technique")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "scRNA Sequencing" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("scRNA Date of Submission")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
        Columns(colNum + 3).EntireColumn.Hidden = True
        Columns(colNum + 4).EntireColumn.Hidden = True
        Columns(colNum + 5).EntireColumn.Hidden = True
        Columns(colNum + 6).EntireColumn.Hidden = True
        Columns(colNum + 7).EntireColumn.Hidden = True
        Columns(colNum + 8).EntireColumn.Hidden = True
        Columns(colNum + 9).EntireColumn.Hidden = True
        Columns(colNum + 10).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
        Columns(colNum + 5).EntireColumn.Hidden = False
        Columns(colNum + 6).EntireColumn.Hidden = False
        Columns(colNum + 7).EntireColumn.Hidden = False
        Columns(colNum + 8).EntireColumn.Hidden = False
        Columns(colNum + 9).EntireColumn.Hidden = False
        Columns(colNum + 10).EntireColumn.Hidden = False
    End If

End Sub


Sub show_scRNA_Sequencing_Info()
    ' show Sorting Info

    colNum = ColumnNumber("scRNA Date of Submission")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
    Columns(colNum + 3).EntireColumn.Hidden = False
    Columns(colNum + 4).EntireColumn.Hidden = False
    Columns(colNum + 5).EntireColumn.Hidden = False
    Columns(colNum + 6).EntireColumn.Hidden = False
    Columns(colNum + 7).EntireColumn.Hidden = False
    Columns(colNum + 8).EntireColumn.Hidden = False
    Columns(colNum + 9).EntireColumn.Hidden = False
    Columns(colNum + 10).EntireColumn.Hidden = False
End Sub


Sub show_hide_PPBC_Info()
    ' Show or hide columns based on "Tissue Type is FFPE Block OR Tissue Type is Frozen Tissue"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Tissue Type")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "FFPE Block" Or Cells(ii, triggerColNum).Value = "Frozen Tissue" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("PPBC Bank #")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
        Columns(colNum + 3).EntireColumn.Hidden = True
        Columns(colNum + 4).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
    End If

End Sub


Sub show_PPBC_Info()
    ' show PPBC Info

    colNum = ColumnNumber("PPBC Bank #")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
    Columns(colNum + 3).EntireColumn.Hidden = False
    Columns(colNum + 4).EntireColumn.Hidden = False
End Sub

Sub show_hide_WGS_Bulk_Info()
    ' Show or hide columns based on "Downstream Submission is WGS Bulk"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("PPBC Downstream Submission")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "WGS Bulk Tumour" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("Date requested from PPBC")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
    End If

End Sub


Sub show_WGS_Bulk_Info()
    ' show WGS Bulk Info

    colNum = ColumnNumber("Date requested from PPBC")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False

End Sub


Sub show_hide_Curls_Info()
    ' Show or hide columns based on "Sectioning Type is Curls"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Sectioning Type")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Curls" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("# of Curls Cut")

    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
    End If

    colNum = ColumnNumber("Concentration (ng/ul)")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
        Columns(colNum + 3).EntireColumn.Hidden = True
        Columns(colNum + 4).EntireColumn.Hidden = True
        Columns(colNum + 5).EntireColumn.Hidden = True
        Columns(colNum + 6).EntireColumn.Hidden = True
        Columns(colNum + 7).EntireColumn.Hidden = True
        Columns(colNum + 8).EntireColumn.Hidden = True
        Columns(colNum + 9).EntireColumn.Hidden = True
        Columns(colNum + 10).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
        Columns(colNum + 5).EntireColumn.Hidden = False
        Columns(colNum + 6).EntireColumn.Hidden = False
        Columns(colNum + 7).EntireColumn.Hidden = False
        Columns(colNum + 8).EntireColumn.Hidden = False
        Columns(colNum + 9).EntireColumn.Hidden = False
        Columns(colNum + 10).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Curls_Info()
    ' show Curls Info

    colNum = ColumnNumber("# of Curls Cut")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False

    colNum = ColumnNumber("Concentration (ng/ul)")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
    Columns(colNum + 3).EntireColumn.Hidden = False
    Columns(colNum + 4).EntireColumn.Hidden = False
    Columns(colNum + 5).EntireColumn.Hidden = False
    Columns(colNum + 6).EntireColumn.Hidden = False
    Columns(colNum + 7).EntireColumn.Hidden = False
    Columns(colNum + 8).EntireColumn.Hidden = False
    Columns(colNum + 9).EntireColumn.Hidden = False
    Columns(colNum + 10).EntireColumn.Hidden = False

End Sub


Sub show_hide_Microdissection_Info()
    ' Show or hide columns based on "Sectioning Type is Microdissect"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Sectioning Type")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Microdissect" Then
            Hide = False
        End If
        If Cells(ii, triggerColNum).Value = "Curls" Then
            Exit Sub    ' becasue this method is called after show_hide_Curls_Info and we don't want it to also run when Curls is chosen
        End If
    Next

    colNum = ColumnNumber("# slides cut for Microdissection")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
        Columns(colNum + 3).EntireColumn.Hidden = True
        Columns(colNum + 4).EntireColumn.Hidden = True
        Columns(colNum + 5).EntireColumn.Hidden = True
        Columns(colNum + 6).EntireColumn.Hidden = True
        Columns(colNum + 7).EntireColumn.Hidden = True
        Columns(colNum + 8).EntireColumn.Hidden = True
        Columns(colNum + 9).EntireColumn.Hidden = True
        Columns(colNum + 10).EntireColumn.Hidden = True
        Columns(colNum + 11).EntireColumn.Hidden = True
        Columns(colNum + 12).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
        Columns(colNum + 5).EntireColumn.Hidden = False
        Columns(colNum + 6).EntireColumn.Hidden = False
        Columns(colNum + 7).EntireColumn.Hidden = False
        Columns(colNum + 8).EntireColumn.Hidden = False
        Columns(colNum + 9).EntireColumn.Hidden = False
        Columns(colNum + 10).EntireColumn.Hidden = False
        Columns(colNum + 11).EntireColumn.Hidden = False
        Columns(colNum + 12).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Microdissection_Info()
    ' show Microdissection_Info

    colNum = ColumnNumber("# slides cut for Microdissection")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
    Columns(colNum + 3).EntireColumn.Hidden = False
    Columns(colNum + 4).EntireColumn.Hidden = False
    Columns(colNum + 5).EntireColumn.Hidden = False
    Columns(colNum + 6).EntireColumn.Hidden = False
    Columns(colNum + 7).EntireColumn.Hidden = False
    Columns(colNum + 8).EntireColumn.Hidden = False
    Columns(colNum + 9).EntireColumn.Hidden = False
    Columns(colNum + 10).EntireColumn.Hidden = False
    Columns(colNum + 11).EntireColumn.Hidden = False
    Columns(colNum + 12).EntireColumn.Hidden = False
End Sub


'Sub show_hide_Extraction_Info()
'    ' Show or hide columns based on "Sectioning Type is Microdissect OR Sectioning Type is Curls"
'
'    Dim LastRow As Long
'    Dim rng As Range
'
'    ' Use all cells on the sheet
'    Set rng = Sheets("Main Database").Cells
'
'    ' Find the last cell
'    LastRow = Last(1, rng)
'
'    triggerColNum = ColumnNumber("Sectioning Type")
'    Hide = True
'    For ii = 6 To LastRow
'        If Cells(ii, triggerColNum).Value = "Microdissect" Or Cells(ii, triggerColNum).Value = "Curls" Then
'            Hide = False
'        End If
'    Next
'
'    colNum = ColumnNumber("Concentration (ng/ul)")
'    If Hide = True Then
'        Columns(colNum).EntireColumn.Hidden = True
'        Columns(colNum + 1).EntireColumn.Hidden = True
'    Else
'        Columns(colNum).EntireColumn.Hidden = False
'        Columns(colNum + 1).EntireColumn.Hidden = False
'    End If
'
'End Sub


'Sub show_Extraction_Info()
    ' show Microdissection_Info

'    colNum = ColumnNumber("Concentration (ng/ul)")
'    Columns(colNum).EntireColumn.Hidden = False
'    Columns(colNum + 1).EntireColumn.Hidden = False
'End Sub


'Sub show_hide_WGS_Bulk_Sequencing_Info()
'    ' Show or hide columns based on "Sectioning Type is Microdissect OR Sectioning Type is Curls"
'
'    Dim LastRow As Long
'    Dim rng As Range
'
'    ' Use all cells on the sheet
'    Set rng = Sheets("Main Database").Cells
'
'    ' Find the last cell
'    LastRow = Last(1, rng)
'
'    triggerColNum = ColumnNumber("Sectioning Type")
'    Hide = True
'    For ii = 6 To LastRow
'        If Cells(ii, triggerColNum).Value = "Microdissect" Or Cells(ii, triggerColNum).Value = "Curls" Then
'            Hide = False
'        End If
'    Next
'
'    colNum = ColumnNumber("WGS Date of Submission")
'    If Hide = True Then
'        Columns(colNum).EntireColumn.Hidden = True
'        Columns(colNum + 1).EntireColumn.Hidden = True
'        Columns(colNum + 2).EntireColumn.Hidden = True
'        Columns(colNum + 3).EntireColumn.Hidden = True
'        Columns(colNum + 4).EntireColumn.Hidden = True
'        Columns(colNum + 5).EntireColumn.Hidden = True
'        Columns(colNum + 6).EntireColumn.Hidden = True
'        Columns(colNum + 7).EntireColumn.Hidden = True
'    Else
'        Columns(colNum).EntireColumn.Hidden = False
'        Columns(colNum + 1).EntireColumn.Hidden = False
'        Columns(colNum + 2).EntireColumn.Hidden = False
'        Columns(colNum + 3).EntireColumn.Hidden = False
'        Columns(colNum + 4).EntireColumn.Hidden = False
'        Columns(colNum + 5).EntireColumn.Hidden = False
'        Columns(colNum + 6).EntireColumn.Hidden = False
'        Columns(colNum + 7).EntireColumn.Hidden = False
'    End If
'
'End Sub


'Sub show_WGS_Bulk_Sequencing_Info()
'    ' show Microdissection_Info
'
'    colNum = ColumnNumber("WGS Date of Submission")
'    Columns(colNum).EntireColumn.Hidden = False
'    Columns(colNum + 1).EntireColumn.Hidden = False
'    Columns(colNum + 2).EntireColumn.Hidden = False
'    Columns(colNum + 3).EntireColumn.Hidden = False
'    Columns(colNum + 4).EntireColumn.Hidden = False
'    Columns(colNum + 5).EntireColumn.Hidden = False
'    Columns(colNum + 6).EntireColumn.Hidden = False
'    Columns(colNum + 7).EntireColumn.Hidden = False
'End Sub


Sub show_hide_IF_Info()
    ' Show or hide columns based on "PPBC Downstream Submission is IF"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("PPBC Downstream Submission")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "IF" Then
            Hide = False
        End If
    Next


    colNum = ColumnNumber("IF Date of Submission")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
    End If

End Sub


Sub show_IF_Info()
    ' show IF Info

    colNum = ColumnNumber("IF Date of Submission")
    Columns(colNum).EntireColumn.Hidden = False
    Columns(colNum + 1).EntireColumn.Hidden = False
    Columns(colNum + 2).EntireColumn.Hidden = False
End Sub


Sub show_hide_Storage_Population()
    ' Show or hide columns based on "Downstream Submission is Storage Only"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Downstream Submission")
    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "Storage Only" Then
            Hide = False
        End If
    Next


    colNum = ColumnNumber("Storage Populations")
    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
    End If

End Sub


Sub show_Storage_Population()
    ' show Storage Population

    colNum = ColumnNumber("Storage Populations")
    Columns(colNum).EntireColumn.Hidden = False
End Sub


Sub show_hide_DLP_Sequencing_Info()
    ' Show or hide columns based on "Sequencing Technique is DLP"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("Sequencing Technique")

    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "DLP" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("DLP Date of Submission")

    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
    End If

End Sub


Sub show_DLP_Sequencing_Info()
    ' show DLP Sequencing Info

    colNum = ColumnNumber("DLP Date of Submission")
    Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
End Sub


Sub show_hide_MSK_DLP_Sequencing_Info()
    ' Show or hide columns based on "DLP Sequencing Location is IGO"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("DLP Sequencing Location")

    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "IGO" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("DLP IGO ID")

    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
        Columns(colNum + 2).EntireColumn.Hidden = True
        Columns(colNum + 3).EntireColumn.Hidden = True
        Columns(colNum + 4).EntireColumn.Hidden = True
        Columns(colNum + 5).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
        Columns(colNum + 5).EntireColumn.Hidden = False
    End If

End Sub


Sub show_MSK_DLP_Sequencing_Info()
    ' show MSK DLP Sequencing Info

    colNum = ColumnNumber("DLP IGO ID")
    Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
        Columns(colNum + 2).EntireColumn.Hidden = False
        Columns(colNum + 3).EntireColumn.Hidden = False
        Columns(colNum + 4).EntireColumn.Hidden = False
        Columns(colNum + 5).EntireColumn.Hidden = False
End Sub


Sub show_hide_BCCRC_DLP_Sequencing_Info()
    ' Show or hide columns based on "DLP Sequencing Location is BCCRC"

    Dim LastRow As Long
    Dim rng As Range

    ' Use all cells on the sheet
    Set rng = Sheets("Main Database").Cells

    ' Find the last cell
    LastRow = Last(1, rng)

    triggerColNum = ColumnNumber("DLP Sequencing Location")

    Hide = True
    For ii = 6 To LastRow
        If Cells(ii, triggerColNum).Value = "BCCRC" Then
            Hide = False
        End If
    Next

    colNum = ColumnNumber("BCCRC Sample ID")

    If Hide = True Then
        Columns(colNum).EntireColumn.Hidden = True
        Columns(colNum + 1).EntireColumn.Hidden = True
    Else
        Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
    End If

End Sub


Sub show_BCCRC_DLP_Sequencing_Info()
    ' show BCCRC DLP Sequencing Info

    colNum = ColumnNumber("BCCRC Sample ID")
    Columns(colNum).EntireColumn.Hidden = False
        Columns(colNum + 1).EntireColumn.Hidden = False
End Sub


' ######### show_hide and show functions END ################


Function ColumnNumber(columnName As String) As Long
    ' Returns the column number for the column with the specified header name.
    ' It is assumed that the header is on row 4 and the maximum number of header columns is less than CA

    ColumnNumber = Sheets("Main Database").Range("A4", "CA4").Find(columnName).Column

End Function



Function Last(choice As Long, rng As Range)
'Ron de Bruin, 5 May 2008
' 1 = last row
' 2 = last column
' 3 = last cell
    Dim lrw As Long
    Dim lCol As Long

    Select Case choice

    Case 1:
        On Error Resume Next
        Last = rng.Find(What:="*", _
                        After:=rng.Cells(1), _
                        Lookat:=xlPart, _
                        LookIn:=xlFormulas, _
                        SearchOrder:=xlByRows, _
                        SearchDirection:=xlPrevious, _
                        MatchCase:=False).Row
        On Error GoTo 0

    Case 2:
        On Error Resume Next
        Last = rng.Find(What:="*", _
                        After:=rng.Cells(1), _
                        Lookat:=xlPart, _
                        LookIn:=xlFormulas, _
                        SearchOrder:=xlByColumns, _
                        SearchDirection:=xlPrevious, _
                        MatchCase:=False).Column
        On Error GoTo 0

    Case 3:
        On Error Resume Next
        lrw = rng.Find(What:="*", _
                       After:=rng.Cells(1), _
                       Lookat:=xlPart, _
                       LookIn:=xlFormulas, _
                       SearchOrder:=xlByRows, _
                       SearchDirection:=xlPrevious, _
                       MatchCase:=False).Row
        On Error GoTo 0

        On Error Resume Next
        lCol = rng.Find(What:="*", _
                        After:=rng.Cells(1), _
                        Lookat:=xlPart, _
                        LookIn:=xlFormulas, _
                        SearchOrder:=xlByColumns, _
                        SearchDirection:=xlPrevious, _
                        MatchCase:=False).Column
        On Error GoTo 0

        On Error Resume Next
        Last = rng.Parent.Cells(lrw, lCol).Address(False, False)
        If Err.Number > 0 Then
            Last = rng.Cells(1).Address(False, False)
            Err.Clear
        End If
        On Error GoTo 0

    End Select
End Function

