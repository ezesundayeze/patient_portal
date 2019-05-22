/**
 * Created by issoftie on 10/30/16.
 */
$.fn.serializeObject = function () {
    var o = {}; // object
    var a = this.serializeArray(); // array
    $.each(a, function () {
        if(o[this.name] !== undefined){
            if(!o[this.name].push){
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        }else{
            o[this.name] = this.value || '';
        }
    });
    return o;
};