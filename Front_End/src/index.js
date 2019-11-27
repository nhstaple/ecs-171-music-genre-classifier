"use strict";

var ajaxRequests = _interopRequireWildcard(require("./ajaxRequests.js"));

var _react = _interopRequireDefault(require("react"));

var _reactDom = _interopRequireDefault(require("react-dom"));

var _pageTwo = _interopRequireDefault(require("./pageTwo.js"));

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

function _getRequireWildcardCache() { if (typeof WeakMap !== "function") return null; var cache = new WeakMap(); _getRequireWildcardCache = function _getRequireWildcardCache() { return cache; }; return cache; }

function _interopRequireWildcard(obj) { if (obj && obj.__esModule) { return obj; } if (obj === null || _typeof(obj) !== "object" && typeof obj !== "function") { return { default: obj }; } var cache = _getRequireWildcardCache(); if (cache && cache.has(obj)) { return cache.get(obj); } var newObj = {}; var hasPropertyDescriptor = Object.defineProperty && Object.getOwnPropertyDescriptor; for (var key in obj) { if (Object.prototype.hasOwnProperty.call(obj, key)) { var desc = hasPropertyDescriptor ? Object.getOwnPropertyDescriptor(obj, key) : null; if (desc && (desc.get || desc.set)) { Object.defineProperty(newObj, key, desc); } else { newObj[key] = obj[key]; } } } newObj.default = obj; if (cache) { cache.set(obj, newObj); } return newObj; }

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

//creaate main page for our application
var MainPage =
/*#__PURE__*/
function (_React$Component) {
  _inherits(MainPage, _React$Component);

  //create constructor for class that holds the page states
  function MainPage(props) {
    var _this;

    _classCallCheck(this, MainPage);

    _this = _possibleConstructorReturn(this, _getPrototypeOf(MainPage).call(this, props)); //State variables for MainPage component

    _defineProperty(_assertThisInitialized(_this), "gotolandingPage", function () {
      _this.setState({
        landingPage: true,
        secondPageState: false
      });
    });

    _defineProperty(_assertThisInitialized(_this), "gotoPageTwoState", function () {
      _this.setState({
        landingPage: false,
        secondPageState: true
      }); //call ajaxrequest, must wait for page to render.


      var song = _this.state.songTitle;
      setTimeout(function () {
        ajaxRequests.sbm(song, 'False');
      }, 1000);
    });

    _defineProperty(_assertThisInitialized(_this), "gotoFeelingLucky", function () {
      _this.setState({
        landingPage: false,
        secondPageState: true
      }); //call ajaxrequest, must wait for page to render.


      var song = _this.state.songTitle;
      setTimeout(function () {
        ajaxRequests.sbm(song, 'True');
      }, 1000);
    });

    _defineProperty(_assertThisInitialized(_this), "handleTextChange", function (event) {
      _this.setState({
        songTitle: event.target.value
      });
    });

    _this.state = {
      landingPage: true,
      secondPageState: false,
      songTitle: '',
      artist: '',
      predictedGenre: '',
      predictedScore: '',
      actualGenre: '',
      actualScore: '',
      modelScore: ''
    };
    return _this;
  } // FUNCTION: gotolandingPage
  // DESCRIPTION: This function indicates that the user should be on the
  // first page by setting the state boolean variables landingPage to
  // true and secondPageState to false.Once these state variables change,
  // the render function will execute and choose what component to show
  // based on these variables.


  _createClass(MainPage, [{
    key: "render",
    // FUNCTION: render
    // DESCRIPTION: The render function is split into two components: 
    // one for the first page(this.state.landingPage === true) and one for the results
    // page(this.state.secondPageState === true).The first page features the input field, 
    // Search button and Feeling Lucky button.The results page calls the < PageTwo /> 
    // component in PageTwo.jsx.The gotolandingPage(), gotoFeelingLucky(), and state
    // variables of index.jsx are passed to the PageTwo component.Note that Index.js
    // is just the React representation of the JSX code from Index.jsx.
    value: function render() {
      //first page
      if (this.state.landingPage === true) {
        return _react.default.createElement("main", null, _react.default.createElement("div", {
          className: "pageContainer"
        }, _react.default.createElement("div", {
          className: "boxContent"
        }, _react.default.createElement("div", {
          className: "title"
        }, _react.default.createElement("div", {
          id: "LandingPage"
        }, "Moosic Classifier"), _react.default.createElement("div", {
          id: "description"
        }, "music genre classifier")), _react.default.createElement("div", {
          id: "textInput"
        }, _react.default.createElement("input", {
          id: "songInput",
          placeholder: "Enter Song Title",
          style: {
            height: 40,
            fontSize: 40
          },
          onChange: this.handleTextChange
        }), _react.default.createElement("div", {
          className: "buttons"
        }, _react.default.createElement("button", {
          id: "buttonStyle",
          onClick: this.gotoPageTwoState
        }, " Search "), _react.default.createElement("button", {
          id: "buttonStyle",
          onClick: this.gotoFeelingLucky
        }, " Feeling Lucky ")))))); //second page
      } else if (this.state.secondPageState === true) {
        return _react.default.createElement(_pageTwo.default, {
          pageState: this.gotolandingPage,
          parentStates: this.state,
          feelingLucky: this.gotoFeelingLucky
        });
      }
    }
  }]);

  return MainPage;
}(_react.default.Component);

_reactDom.default.render(_react.default.createElement(MainPage, null), document.getElementById('root'));