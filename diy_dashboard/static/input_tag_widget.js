// use this format b/c the document.currentScript name creates
// a new string, which is passed by reference to the anon function.
// any callbacks then enclose the ref to the created string (which
// doesn't cause conflicts b/c it is never named and thus can never be
// referred to again elsewhere). The things I do for javascript.
// NB: I think it would also work to do var widgetname = document.cu... inside
// the anon function.
// NB: this could all be avoided by just using Babel (which has module-local scope)
(function(widgetname) {
    FigureWidgets.add(widgetname, FigureWidgets.inputTagWidget);
})(document.currentScript.dataset.widgetname);
