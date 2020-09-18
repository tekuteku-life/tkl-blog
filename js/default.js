
const PC_DEFAULT_CSS = "./css/default.css";
const MOBILE_DEFAULT_CSS = "./css/mobile_default.css";

window.addEventListener("load", function() {
	let ua = navigator.userAgent;
	
	let head = document.querySelector("head");
	let link = head.insertBefore(document.createElement("link"), head.firstChild);
	link.setAttribute("rel", "stylesheet");

	if( (ua.indexOf("iPhone") > 0 || ua.indexOf("Android") > 0) && ua.indexOf("Mobile") > 0 ) {
		link.setAttribute("href", MOBILE_DEFAULT_CSS);
	}
	else {
		link.setAttribute("href", PC_DEFAULT_CSS);
	}
});