if (!$) {
    // Need this line because Django also provided jQuery and namespaced as django.jQuery
    $ = django.jQuery;
}

$(function($) {
    $(function() {
        $("input[name='real_price']").change(function() {
                    // $("select['test_case']").val('');
                    PriceAndPercent();
    });
    });
    $(function() {
        $("input[name='percent_off']").change(function() {
                    // $("select['test_case']").val('');
                    PriceAndPercent();
    });  
});
    function PriceAndPercent(){
        var real_price=$("input[name='real_price']").val();
        var percent_off=$("input[name='percent_off']").val();
        var price=$("input[name='price']");
        price.val(Number(real_price-(real_price*percent_off/100)));
            console.log(price);
    }

});
