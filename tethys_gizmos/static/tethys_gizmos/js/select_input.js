/*****************************************************************************
 * FILE:    select_input.js
 * DATE:    November 2016
 * AUTHOR:  Alan D. Snow
 * LICENSE: BSD 2-Clause
 *****************************************************************************/

/*****************************************************************************
 *                      LIBRARY WRAPPER
 *****************************************************************************/

var TETHYS_SELECT_INPUT = (function() {
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
 	var initSelectInput;

 	initSelectInput = function(tag) {
 	    $(tag).each(function(){
            var options = $(this).data('select2-options');
            $(this).select2(options);
 	    });
 	};

	/************************************************************************
 	*                            TOP LEVEL CODE
 	*************************************************************************/
	/*
	 * Library object that contains public facing functions of the package.
	 */
	public_interface = {
        initSelectInput: initSelectInput,
     };

	// Initialization: jQuery function that gets called when
	// the DOM tree finishes loading
	$(function() {
		// Initialize any select2 elements
		initSelectInput($('.tethys-select2'));
	});

	return public_interface;

}()); // End of package wrapper

/*****************************************************************************
 *                      Public Functions
 *****************************************************************************/

/* This statement for testing coverage purposes */
/* istanbul ignore next */
if (typeof module !== "undefined" && module.exports) {
    module.exports = TETHYS_SELECT_INPUT;
}