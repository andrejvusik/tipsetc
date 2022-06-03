function translate(sourceElem, destElem, sourceLang, destLang) {
    $(destElem).html("<img src='../../static/img/spinner2.gif'>");
    $.post('/translate/title', {
        source_language: sourceLang,
        dest_language: destLang,
        text: $(sourceElem).text()
    }).done(function(response) {
        $(destElem).text(response['text'])
    }).fail(function() {
        $(destElem).text("{{ _('Error: Could not contact server.') }}");
    });
}
