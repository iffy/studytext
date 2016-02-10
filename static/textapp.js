var selected_word = null;

function rpc(method, kwargs) {
  return $.ajax({
    contentType: "application/json",
    data: JSON.stringify({
      'method': method,
      'kwargs': kwargs
    }),
    type: "POST",
    url: "/api/rpc",
  });
}

function placeAsWords(text, element) {
  var parsed = text.split(/(\s+|--)/);
  var word_counts = {};
  element = $(element);
  element.text('');
  for (var i = 0; i < parsed.length; i++) {
    var word = parsed[i];
    if (/\s+/.test(word)) {
      // whitespace
      element.append(word.replace(/\n\n/g, '<br/><br/>'));
    } else {
      // text
      if (!word_counts[word]) {
        word_counts[word] = 0;
      }
      var elem = $('<span>' + word + '</span>')
        .data('tcite', '{' + word + '}' + word_counts[word]);
      element.append(elem);
      if (!selected_word) {
        selectWord(elem);
      }
      word_counts[word] += 1;
    }
  }
  element.click(function(ev) {
    if ($(ev.target)[0] !== $(element)[0]) {
      selectWord($(ev.target));
    }
  })
}

function selectWord(element) {
  if (selected_word) {
    console.log('removing selection', selected_word);
    selected_word.removeClass('selected');
  }
  selected_word = element;
  console.log('selected', element);
  selected_word.addClass('selected');

  console.log(selected_word.position());
  var entry_div = $('<div></div>');
  entry_div.addClass('note-entry')
}