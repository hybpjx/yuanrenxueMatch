var CryptoJS = require('crypto-js');


function sign(page) {


    var t = Date.parse(new Date());
    list = {
        "page": page,
        "sign": CryptoJS.MD5(page + '|' + t.toString() + 'D#uqGdcw41pWeNXm').toString(),
        "t": t,
    }
    return list

}


console.log(sign(1))