function equalize_width ( selector ) {
    var maxWidth = 0;
    var tags = $(selector);

    for (var i = 0; i < tags.length; i++) {
        maxWidth = Math.max($(tags[i]).width(), maxWidth);
    };

    for (var i = 0; i < tags.length; i++) {
        $(tags[i]).width(maxWidth + 10); // 10 px padding
    };
}

$(document).ready( function() {
    $(".information").click(function () {
        $(this).siblings(".error-info").toggle();
    });
    // Hide all error-info divs
    $(".information").click();

    equalize_width(".column-1");
    equalize_width(".column-2");
})
