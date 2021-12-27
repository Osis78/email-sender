$(document).ready(function() {

    function apply_filter() {
        if (filtering_fields.val() != "") {
            filters.val(filters.val() + "`"+filtering_fields.val()+"`" + " ");
        }
        if (filtering_operators.val() != "") {
            filters.val(filters.val() + filtering_operators.val() + " ");
        }
        if (filtering_condition.val() != "") {
            filters.val(filters.val() + "`"+filtering_condition.val()+"`" + " ");
        }
    }

    function remove_filter() {
        filters.val("");
    }

    let editor = $('#emailContent');
    let editorHTML;
    //let selectedColor = $('#contentBgColor').val();

    let apply_filter_bt = $('#apply_filter');
    let remove_filter_bt = $('#remove_filter');
    let filters = $('#filters');
    let filtering_fields = $('#filtering_fields');
    let filtering_operators = $('#filtering_operators');
    let filtering_condition = $('#filtering_condition');
    let and_condition = $('#and_condition');
    let or_condition = $('#or_condition');
    let addVar = $('#addVar');
    //let left_parenthesis = $('#left_parenthesis');
    //let right_parenthesis = $('#right_parenthesis');

    //let add_var_bt = $('#add_var');

    //editor.css('background-color', selectedColor);
    $('#content_title').css('display', 'none');
    $('#content').css('display', 'none');
    //$('#filters').attr('disabled', true);

    $('#emailContent').trumbowyg({
        lang: 'fr',
        imageWidthModalEdit: true,
        urlProtocol: true,
        defaultLinkTarget: '_blank',
        btnsDef: {
            // Create a new dropdown
            image: {
                dropdown: ['insertImage', 'upload'],
                ico: 'insertImage'
            },
        },
        btns: [
            ['viewHTML'],
            ['historyUndo', 'historyRedo'],
            ['formatting'],
            ['fontfamily'],
            ['fontsize'],
            ['strong', 'em', 'del'],
            ['superscript', 'subscript'],
            ['foreColor', 'backColor'],
            ['link'],
            ['emoji'],
            ['image'],
            ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
            ['indent', 'outdent'],
            ['unorderedList', 'orderedList'],
            ['horizontalRule'],
            ['removeformat'],
            ['fullscreen']
        ],
        plugins: {
            fontfamily: {
                fontList: [
                    {name: 'Arial', family: 'Arial, Helvetica, sans-serif'},
                    {name: 'Open Sans', family: '\'Open Sans\', sans-serif'}
                ]
            },
            fontsize: {
                sizeList: [
                    '12px',
                    '14px',
                    '16px',
                    '18px',
                    '24px',
                    '32px',
                    '40px'
                ]
            },
            upload: {
                serverPath: 'plugins/Trumbowyg-main/dist/plugins/upload/upload.php',
            }
        }
    }).on('tbwinit', () => {
        //$('#emailContent').trumbowyg('html', '<div>Test</div>');
    }).on('tbwchange', () => {
        // Get html content in the editor
        editorHTML = $('#emailContent').html();
        $('#content').val('<table cellpadding="16">'+editorHTML+'</table>');
    });

    /*$('#contentBgColor').on('input', () => {
        selectedColor = $('#contentBgColor').val();
        $('#emailContent').css('background-color', selectedColor);
    });*/

    apply_filter_bt.on('click', () => {
        apply_filter();
    });
    remove_filter_bt.on('click', () => {
        remove_filter();
    });
    and_condition.on('click', () => {
        filters.val(filters.val() + "et ");
    });
    or_condition.on('click', () => {
        filters.val(filters.val() + "ou ");
    });
    /*left_parenthesis.on('click', () => {
        filters.val(filters.val() + "(");
    });
    right_parenthesis.on('click', () => {
        filters.val(filters.val() + ")");
    });*/
    addVar.on('click', () => {
        editor.append('{{' + $('#liquidVars').val() + '}}');
    });
});