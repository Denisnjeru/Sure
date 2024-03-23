const customHr = function(editor) {
    // create button
    editor.ui.registry.addButton('hrcustom', {
        text: 'hr',
        tooltip: 'Insert horizontal rule',
        onAction: function() {
            alert('custom hr')
        }
    });
}

export { customHr };