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
      console.log("ATTEMPTING TO LEAVE");

      _this.props.pageState();
    });

    return _this;
  }

  _createClass(PageTwo, [{
    key: "render",
    value: function render() {
      return _react.default.createElement("main", null, _react.default.createElement("div", {
        id: "page_two_contents"
      }, _react.default.createElement("h1", null, _react.default.createElement("div", {
        id: "title_and_artist"
      }, _react.default.createElement("div", {
        id: "songTitle"
      }, this.props.parentStates.songTitle), _react.default.createElement("div", {
        id: "artist"
      }, this.props.parentStates.artist))), _react.default.createElement("button", {
        id: "back_button",
        onClick: this.gotolandingPage
      }, "Go Back"), _react.default.createElement("div", {
        id: "predicted_genre"
      }, _react.default.createElement("div", {
        id: "predicted_genre_name"
      }, _react.default.createElement("p", {
        id: "placeGenreHere"
      })), _react.default.createElement("div", {
        id: "predicted_genre_probability"
      }, this.props.parentStates.predictedScore, " Confidence")), _react.default.createElement("div", {
        id: "actual_genre"
      }, _react.default.createElement("div", {
        id: "actual_genre_name"
      }, "Actual: ", this.props.parentStates.actualGenre), _react.default.createElement("div", {
        id: "actual_genre_probability"
      }, this.props.parentStates.actualScore, " Confidence")), _react.default.createElement("div", {
        id: "model_stats"
      }, _react.default.createElement("img", {
        src: require('./sampleImage.png')
      }), _react.default.createElement("div", {
        id: "model_score"
      }, this.props.parentStates.modelScore))));
    }
  }]);

  return PageTwo;
}(_react.default.Component);

var _default = PageTwo;
exports.default = _default;