$( document ).ready(function() {

    let editor = $('#emailContent');
    let editorHTML;
    let selectedColor = $('#contentBgColor').val();

    editor.css('background-color', selectedColor);
    $('#content_title').css('display', 'none');
    $('#content').css('display', 'none');

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
            }
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
        $('#content').val('<table cellpadding="16" width="500" style="background-color:'+selectedColor+';min-height:300px;">'+editorHTML+'</table>');
        console.log($('#content').val());
    });

    $('#contentBgColor').on('input', () => {
        selectedColor = $('#contentBgColor').val();
        $('#emailContent').css('background-color', selectedColor);
    });

});