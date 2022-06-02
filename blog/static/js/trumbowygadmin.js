$('#editor')
.trumbowyg({
    btnsDef: {
        // Create a new dropdown
        image: {
            dropdown: ['insertImage', 'base64'],
            ico: 'insertImage'
        }
    },

    // Redefine the button pane
    btns: [
        ['viewHTML'],
        ['formatting'],
        ['strong', 'em', 'del'],
        ['foreColor', 'backColor'],
        ['superscript', 'subscript'],
        ['link'],
        ['image'], // Our fresh created dropdown
        ['justifyLeft', 'justifyCenter', 'justifyRight', 'justifyFull'],
        ['unorderedList', 'orderedList'],
        ['horizontalRule'],
        ['removeformat'],
        ['fullscreen']
    ],

    plugins: {
        resizimg: {
            minSize: 64,
            step: 16,
        }
    }
  });
