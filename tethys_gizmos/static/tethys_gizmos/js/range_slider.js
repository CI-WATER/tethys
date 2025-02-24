/*****************************************************************************
 * FILE:    range_slider.js
 * DATE:    November 2016
 * AUTHOR:  Alan D. Snow
 * LICENSE: BSD 2-Clause
 *****************************************************************************/

/*****************************************************************************
 *                      LIBRARY WRAPPER
 *****************************************************************************/

var TETHYS_RANGE_SLIDER = (function() {
	// Wrap the library in a package function
	"use strict"; // And enable strict mode for this library

	/************************************************************************
 	*                      MODULE LEVEL / GLOBAL VARIABLES
 	*************************************************************************/
 	var public_interface;				// Object returned by the module

     /************************************************************************
 	*                    PRIVATE FUNCTION DECLARATIONS
 	*************************************************************************/
 	// private methods
 	var init_range_sliders;

 	init_range_sliders = function() {
		document.querySelectorAll('.form-range').forEach(element => {
			element.addEventListener('input', function(e){
				element.nextElementSibling.innerHTML = element.value;
			});
		});
 	};

	/************************************************************************
 	*                            TOP LEVEL CODE
 	*************************************************************************/
	/*
	 * Library object that contains public facing functions of the package.
	 */
	// TODO Make sure this is ok
	public_interface = {
		init_range_sliders: init_range_sliders,
	};

	// Initialization: jQuery function that gets called when
	// the DOM tree finishes loading
	$(function() {
		init_range_sliders();
	});

	return public_interface;

}()); // End of package wrapper

/* This statement for testing coverage purposes */
/* istanbul ignore next */
if (typeof module !== "undefined" && module.exports) {
	module.exports = TETHYS_RANGE_SLIDER;
}