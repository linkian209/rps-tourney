$(document).ready(function(){
    // First adjust the height
    var nav_height = $('#navbar').outerHeight();
    $('#main_content').css('height', 'calc(100% - ' + nav_height + 'px)');

    // Now set up mutation observer
    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === "class") {
                var attributeValue = $(mutation.target).prop(mutation.attributeName);
                if(attributeValue.indexOf("collapsing") == -1)
                {
                    var nav_height = $('#navbar').outerHeight();
                    $('#main_content').css('height', 'calc(100% - ' + nav_height + 'px)');
                }
            }
        });
    });
    observer.observe($('#navbarSupportedContent')[0], {attributes: true});
});