/*
* To try in Ace editor, copy and paste into the mode creator
* here : http://ace.c9.io/tool/mode_creator.html
*/

define(function(require, exports, module) {
"use strict";
var oop = require("../lib/oop");
var TextHighlightRules = require("./text_highlight_rules").TextHighlightRules;
/* --------------------- START ----------------------------- */
var StackscriptHighlightRules = function() {
this.$rules = {
"start" : [
   {
      "token" : "comment",
      "regex" : "(//.*)"
   },
   {
      "token" : "text",
      "regex" : "(!\\B|%\\B|&\\B|\\*\\B|\\*\\*\\B|\\+\\B|-\\B|\\/\\B|<\\B|<<\\B|<=\\B|=\\B|>\\B|>=\\B|>>\\B|@\\B|\\^\\B|\\|\\B|~\\B)"
   },
   {
      "token" : "text",
      "regex" : "(break\\b|continue\\b|delete\\b|do\\b|else\\b|end\\b|func\\b |global\\b|if\\b|return\\b|store\\b|update\\b|while\\b)"
   },
   {
      "token" : "text",
      "regex" : "(clear\\b|collect\\b|drop\\b|dump\\b|dup\\b|exit\\b|expand\\b|import\\b|in\\b|index\\b|len\\b|out\\b|outln\\b|pull\\b|push\\b|rem\\b|sqrt\\b|stacklen\\b|sth\\b|swap\\b|trace\\b)"
   },
   {
      "token" : "constant.numeric",
      "regex" : "(true\\b|false\\b)"
   },
   {
      "token" : "constant.numeric",
      "regex" : "(\\b\\d+)"
   },
   {
      "token" : "invalid",
      "regex" : "(std\\b|math\\b|builtins\\b|os\\b|types\\b|io\\b)"
   },
   {
      "token" : "text",
      "regex" : "(\\\")",
      "push" : "main__1"
   },
   {
      "token" : "text",
      "regex" : "(\\')",
      "push" : "main__2"
   },
   {
      "token" : "keyword",
      "regex" : "(\\b[a-z][a-z0-9]*)"
   },
   {
      defaultToken : "text",
   }
],
"main__1" : [
   {
      "token" : "text",
      "regex" : "(\\\")",
      "next" : "pop"
   },
   {
      defaultToken : "text",
   }
],
"main__2" : [
   {
      "token" : "text",
      "regex" : "(\\')",
      "next" : "pop"
   },
   {
      defaultToken : "text",
   }
]
};
this.normalizeRules();
};
/* ------------------------ END ------------------------------ */
oop.inherits(StackscriptHighlightRules, TextHighlightRules);
exports.StackscriptHighlightRules = StackscriptHighlightRules;
});
