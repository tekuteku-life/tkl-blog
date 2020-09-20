
const MOBILE_REV_CSS = "./css/mobile_rev.css";

window.addEventListener("load", function() {
	let ua = navigator.userAgent;

	if( (ua.indexOf("iPhone") > 0 || ua.indexOf("Android") > 0) && ua.indexOf("Mobile") > 0 ) {
		let head = document.querySelector("head");
		let link = head.insertBefore(document.createElement("link"), head.firstChild);
		link.setAttribute("rel", "stylesheet");
		link.setAttribute("href", MOBILE_REV_CSS);
	}
});