/*  ------------------------------------------------------------------
    Split Phone field in 3 fields ------------------------------------ */
$.fn.splitPhone = function() {
    function phone_split(phoneId){
        var html_split = '<input type="text" name="'+phoneId+'[]" id="'+phoneId+'1" class="phone_part" value="" size="4" maxlength="3" tabindex="0" /><span class="sep_phone"> - </span>';
            html_split += '<input type="text" name="'+phoneId+'[]" id="'+phoneId+'2" class="phone_part" value="" size="4" maxlength="3" tabindex="1" /><span class="sep_phone"> - </span>';
            html_split += '<input type="text" name="'+phoneId+'[]" id="'+phoneId+'3" class="phone_part_last" value="" size="5" maxlength="4" tabindex="2" />';
        return html_split;
    }

    this.each(function() {
        var $this = $(this);
        if (!($this.is(':text') || $this.is(':hidden'))) { return; }
        var tabIndex = $this.attr("tabindex") ? $this.attr("tabindex") : 0;

        //Custom new fields
        var $arrInput = $(phone_split($this.attr("id"))).filter("input");
        $arrInput.each(function(){ $(this).attr("tabindex", tabIndex) }).bind("keyup", function(){ $this.val($arrInput[0].value+$arrInput[1].value+$arrInput[2].value) }).end().insertBefore($this);

        //hide fields
        $this.attr("Type", "hidden").removeAttr("tabindex").hide();
    });

    return this;
};
