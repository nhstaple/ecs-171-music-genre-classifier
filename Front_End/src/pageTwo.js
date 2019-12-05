"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
exports.default = void 0;

var _react = _interopRequireDefault(require("react"));

var _reactDom = _interopRequireDefault(require("react-dom"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _typeof(obj) { if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; }

var PageTwo =
/*#__PURE__*/
function (_React$Component) {
  _inherits(PageTwo, _React$Component);

  function PageTwo(props) {
    var _this;

    _classCallCheck(this, PageTwo);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(PageTwo).call(this, props));

    _defineProperty(_assertThisInitialized(_this), "gotolandingPage", function () {
      _this.props.pageState();
    });

    _defineProperty(_assertThisInitialized(_this), "gotoFeelingLucky", function () {
      //clear page while loading new song
      document.getElementById('songName').textContent = '';
      document.getElementById('artist').textContent = '';
      document.getElementById('genre_rank_1').textContent = 'LOADING...';
      document.getElementById('probability_rank_1').textContent = '';
      document.getElementById('genre_rank_2').textContent = '';
      document.getElementById('probability_rank_2').textContent = '';
      document.getElementById('genre_rank_3').textContent = '';
      document.getElementById('probability_rank_3').textContent = '';
      document.getElementById('genre_rank_4').textContent = '';
      document.getElementById('probability_rank_4').textContent = '';
      document.getElementById('genre_rank_5').textContent = '';
      document.getElementById('probability_rank_5').textContent = '';
      document.getElementById('genre_rank_6').textContent = '';
      document.getElementById('probability_rank_6').textContent = '';
      document.getElementById('genre_rank_7').textContent = '';
      document.getElementById('probability_rank_7').textContent = '';
      document.getElementById('genre_rank_8').textContent = '';
      document.getElementById('probability_rank_8').textContent = '';
      document.getElementById('actualGenre').textContent = '';
      document.getElementById('songScore').textContent = '';
      document.getElementById('actualScore').textContent = '';
      document.getElementById('modelScore').textContent = '';
      document.getElementById('redirect_link').textContent = '';
      document.getElementById("genre_rank_1").style.backgroundColor = "";
      document.getElementById("probability_rank_1").style.backgroundColor = "";
      document.getElementById("genre_rank_2").style.backgroundColor = "";
      document.getElementById("probability_rank_2").style.backgroundColor = "";
      document.getElementById("genre_rank_3").style.backgroundColor = "";
      document.getElementById("probability_rank_3").style.backgroundColor = "";
      document.getElementById("genre_rank_4").style.backgroundColor = "";
      document.getElementById("probability_rank_4").style.backgroundColor = "";
      document.getElementById("genre_rank_5").style.backgroundColor = "";
      document.getElementById("probability_rank_5").style.backgroundColor = "";
      document.getElementById("genre_rank_6").style.backgroundColor = "";
      document.getElementById("probability_rank_6").style.backgroundColor = "";
      document.getElementById("genre_rank_7").style.backgroundColor = "";
      document.getElementById("probability_rank_7").style.backgroundColor = "";
      document.getElementById("genre_rank_8").style.backgroundColor = "";
      document.getElementById("probability_rank_8").style.backgroundColor = "";

      _this.props.feelingLucky();
    });

    return _this;
  } // FUNCTION: gotolandingPage
  // DESCRIPTION: This function wraps the gotolandingPage 
  // function of index.jsx.It will get called when the Go 
  // Back button is pushed.


  _createClass(PageTwo, [{
    key: "render",
    // FUNCTION: render
    // DESCRIPTION: This function returns JSX code that will build 
    // the HTML for the results page.This page features the song 
    // title, artist, predicted genre, predicted genre probability, 
    // actual genre, actual genre probability, song rank and model 
    // rank.There is also a back button that goes back to the first 
    // page, random button that will reroll results for a random song, 
    // and a YouTube search link that will search for the given song and 
    // artist.When there is initially no data, the predicted genre text 
    // is replaced with 'Loading...' until a response is received from 
    // the backend.
    value: function render() {
      //page two contents
      return _react.default.createElement("main", null, _react.default.createElement("div", {
        id: "page_two_contents"
      }, _react.default.createElement("h1", null, _react.default.createElement("div", {
        id: "title_and_artist"
      }, _react.default.createElement("div", {
        id: "songTitle"
      }, _react.default.createElement("p", {
        id: "songName"
      })), _react.default.createElement("div", {
        id: "artist"
      }, _react.default.createElement("p", {
        id: "artist"
      })))), _react.default.createElement("button", {
        id: "back_button",
        onClick: this.gotolandingPage
      }, "Go Back"), _react.default.createElement("button", {
        id: "random_button",
        onClick: this.gotoFeelingLucky
      }, " Random Song "), _react.default.createElement("div", {
        id: "results_wrapper"
      }, _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_1"
      }, "LOADING...")), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_1"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_2"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_2"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_3"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_3"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_4"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_4"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_5"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_5"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_6"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_6"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_7"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_7"
      }))), _react.default.createElement("div", {
        className: "predicted_genre"
      }, _react.default.createElement("div", {
        className: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "genre_rank_8"
      })), _react.default.createElement("div", {
        className: "predicted_genre_probability"
      }, _react.default.createElement("p", {
        id: "probability_rank_8"
      })))), _react.default.createElement("div", {
        id: "actual_genre"
      }, _react.default.createElement("div", {
        id: "actual_genre_name"
      }, _react.default.createElement("p", {
        id: "actualGenre"
      })), _react.default.createElement("div", {
        id: "actual_genre_probability"
      }, _react.default.createElement("p", {
        id: "actualScore"
      }))), _react.default.createElement("div", {
        id: "song_stats"
      }, _react.default.createElement("div", {
        id: "song_score"
      }, _react.default.createElement("p", {
        id: "songScore"
      }))), _react.default.createElement("div", {
        id: "model_stats"
      }, _react.default.createElement("div", {
        id: "model_score"
      }, _react.default.createElement("p", {
        id: "modelScore"
      }))), _react.default.createElement("a", {
        id: "redirect_link",
        style: {
          display: "table-cell"
        },
        href: "",
        target: "_blank"
      })));
    }
  }]);

  return PageTwo;
}(_react.default.Component);

var _default = PageTwo;
exports.default = _default;