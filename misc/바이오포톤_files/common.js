$(function(){
	common.header();
    //common.footer();
    common.pop();
    common.popOpen();
    common.popClose();
    common.etcEvt();
    common.aosInit();
});


var TOUCH = "ontouchstart" in window;
var tevent = '';
if (TOUCH){
    tevent = "touchstart";
}else{
    tevent = "click";
}

//모바일 화면 높이
let vh = window.innerHeight * 0.01
document.documentElement.style.setProperty('--vh', `${vh}px`)
window.addEventListener('resize', () => {
  let vh = window.innerHeight * 0.01
  document.documentElement.style.setProperty('--vh', `${vh}px`)
});

common = {
    calendar:function(){
        $(".datepicker").datepicker({
            dateFormat: "yy / mm / dd (DD)",
            dayNamesMin: ['월', '화', '수', '목', '금', '토', '일'],
            dayNames: ['월', '화', '수', '목', '금', '토', '일'],
            dayNamesShort: ['월', '화', '수', '목', '금', '토', '일'],
        });
    },
	header:function(){
        //$('header').load('../header.html');
        //$('nav').load('../nav_mob.html');

        $(document).on('click','.btn_menu',function(){
            $('.nav_mob').show();
        });
    
        $(document).on('click','.close_menu',function(){
            $('.nav_mob').hide();
        });
    },
    footer:function(){
        $('footer').load('../footer.html');
    },
    pop:function(){
        $('#sub0202_pop').load('../popup/sub0202_pop.html');
        $('#sub0203_pop').load('../popup/sub0203_pop.html');
        $('#sub0204_pop').load('../popup/sub0204_pop.html');
		$('#e_sub0202_pop').load('../popup/e_sub0202_pop.html');
        $('#e_sub0203_pop').load('../popup/e_sub0203_pop.html');
        $('#e_sub0204_pop').load('../popup/e_sub0204_pop.html');
		$('#c_sub0202_pop').load('../popup/c_sub0202_pop.html');
        $('#c_sub0203_pop').load('../popup/c_sub0203_pop.html');
        $('#c_sub0204_pop').load('../popup/c_sub0204_pop.html');
        //$('#product_ask').load('write.php?bo_table=qa');
    },
    aosInit:function(){
        AOS.init({
            duration: 1000,
            easing: 'linear',
            once: true,
        });
    },
    etcEvt:function(){


    },
	//팝업
    popOpen:function(o){
        $(o).addClass("on");
        setTimeout(function(){
            $(o).addClass("ing");
        },100);
        $('html').css('overflow','hidden');
    },
    popClose:function(o){
        $(o).removeClass("ing");
        $(o).removeClass("on");
		$('html').css('overflow','auto');
        $('.pop_stl02').find('.img_wrap img').attr('src', '');
        $('.pop_stl02 .img_file label').removeClass('on');
    },
}
