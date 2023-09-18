$(function(){
    // Defaults
    var l = '2';
    var n = '50';
    var m = '2';
    var p = '0';
    var q = '0';
    var z = '20';
    var noises = '5 10 15 20';
    //
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        enableAllSteps: true,
        forceMoveForward: false,
        transitionEffectSpeed: 500,
        titleTemplate : '<span class="title">#title#</span>',
        labels: {
            previous : 'Previous',
            next : 'Next',
            finish : 'Generate!',
            current: ''
        },

        onStepChanging: function (event, currentIndex, newIndex) {
            if ( $('#dataset_name').val() == '' ){
                $("#dataset_name").css('border-color', 'red');
                return false;
            } else {
                $("#dataset_name").css('border-color', '');
            }

            $('#dataset_name-val').text( $('#dataset_name').val() );
            $('#ntype-val').text( $('#ntype').val() );
            $('#l-val').text( (($('#l').val() == '') ? l : $('#l').val()) );
            $('#n-val').text( (($('#n').val() == '') ? n : $('#n').val()) );
            $('#m-val').text( (($('#m').val() == '') ? m : $('#m').val()) );
            $('#p-val').text( (($('#p').val() == '') ? p : $('#p').val()) );
            $('#q-val').text( (($('#q').val() == '') ? q : $('#q').val()) );
            $('#z-val').text( (($('#z').val() == '') ? z : $('#z').val()) );
            $('#noises-val').text( (($('#noises').val() == '') ? noises : $('#noises').val()) );

            return true;
        },

        onFinishing: function(e, currentIndex) {
            var formData = '{' + 
                '"dataset_name" : "' + $('#dataset_name').val() + '",' +
                '"ntype" : "' + $('#ntype').val() + '",' +
                '"l" : "' + (($('#l').val() == '') ? l : $('#l').val()) + '",' +
                '"n" : "' + (($('#n').val() == '') ? n : $('#n').val()) + '",' +
                '"m" : "' + (($('#m').val() == '') ? m : $('#m').val()) + '",' +
                '"p" : "' + (($('#p').val() == '') ? p : $('#p').val()) + '",' +
                '"q" : "' + (($('#q').val() == '') ? q : $('#q').val()) + '",' +
                '"z" : "' + (($('#z').val() == '') ? z : $('#z').val()) + '",' +
                '"noises" : "' + (($('#noises').val() == '') ? noises : $('#noises').val()) + '"' + 
                '}';

            $.ajax({
                type: "POST",
                url: "/generate",
                data: JSON.stringify(formData),
                contentType: 'application/json',
                xhrFields: {
                    responseType: 'blob' // to avoid binary data being mangled on charset conversion
                },
                success: function(blob, status, xhr) {
                    var filename = JSON.parse(formData)['dataset_name'];

                    var disposition = xhr.getResponseHeader('Content-Disposition');
                    if (disposition && disposition.indexOf('attachment') !== -1) {
                        var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                        var matches = filenameRegex.exec(disposition);
                        if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                    }
            
                    if (typeof window.navigator.msSaveBlob !== 'undefined') {
                        // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                        window.navigator.msSaveBlob(blob, filename);
                    } else {
                        var URL = window.URL || window.webkitURL;
                        var downloadUrl = URL.createObjectURL(blob);
            
                        if (filename) {
                            // use HTML5 a[download] attribute to specify filename
                            var a = document.createElement("a");
                            // safari doesn't support this yet
                            if (typeof a.download === 'undefined') {
                                window.location.href = downloadUrl;
                            } else {
                                a.href = downloadUrl;
                                a.download = filename;
                                document.body.appendChild(a);
                                a.click();
                            }
                        } else {
                            window.location.href = downloadUrl;
                        }
            
                        setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
                    }
                },
                error: function (textStatus, errorThrown) {
                    console.log(textStatus);
                    console.log(errorThrown);
                }
            });         
        },
        onFinished: function(e, currentIndex) {
            return true;
        }
    });
});