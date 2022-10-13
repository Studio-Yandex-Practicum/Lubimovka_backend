// JS-based Typograf: https://github.com/typograf/typograf
// ckeditor plugin integration provided by: https://github.com/vgrish/ckeditor-plugin-typograf/

(function () {

	if (CKEDITOR.plugins.get('typograf')) {
		return false;
	}

	CKEDITOR.plugins.add('typograf', {

		lang: 'en,ru',
		icons: 'typograf',
		hidpi: true,
		init: function (editor) {
			var pluginName = 'typograf',
				config = {},
				tp;

			var rx = new RegExp(pluginName + '_');
			for (var i in editor.config) {
				if (!editor.config.hasOwnProperty(i)) {
					continue;
				}
				if (!rx.test(i)) {
					continue;
				}
				config[i.replace(pluginName + '_', '')] = editor.config[i];
			}

			if (!config['pathTypograf']) {
				config['pathTypograf'] = 'vendor/typograf/dist/typograf.min.js';
			}

			CKEDITOR.scriptLoader.load(CKEDITOR.plugins.getPath(pluginName) + config['pathTypograf'], function () {

				tp = new Typograf({
					lang: CKEDITOR.lang.detect(),
					mode: 'name'
				});

				if (config['addSafeTag']) {
					config['addSafeTag'].filter(function (tags) {
						switch (tags.length) {
							case 1:
								tp.addSafeTag(eval(tags[0][0]));
								break;
							case 2:
								tp.addSafeTag(tags[0][0], tags[1][0]);
								break;
							case 3:
								tp.addSafeTag(tags[0][0], tags[1][0], tags[2][0]);
								break;
						}
					});
				}
			});

			editor.addCommand(pluginName, {
				exec: function (e) {

					if (!tp) {
						return;
					}

					var sel = e.getSelection(),
						frag = e.getSelectedHtml(),
						html = frag.getHtml();

					if (CKEDITOR.env.ie) {
						sel.root.fire('selectionchange');
					}

					if (html != '') {
						e.insertHtml(tp.execute(html));
					}

				},
				modes: {wysiwyg: 1},
				canUndo: true
			});

			editor.ui.addButton && editor.ui.addButton('Typograf', {
				label: editor.lang.typograf.toolbar,
				command: pluginName,
				toolbar: 'doctools,50'
			});

		}
	});

})();
