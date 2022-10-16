import { Form } from "@quillforms/renderer-core";
import { useState } from 'react'
import "@quillforms/renderer-core/build-style/style.css";
import axios from "axios"
import { registerCoreBlocks } from "@quillforms/react-renderer-utils";
import "./styles.css";

registerCoreBlocks();
const App = () => {
  const [profileData, setProfileData] = useState(null)

  function getData() {
    axios({
      method: "GET",
      url:"/profile",
    })
    .then((response) => {
      const res =response.data
      setProfileData(({
        profile_name: res.name,
        about_me: res.about}))
    }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
        }
    })}
  
  return (
    <div style={{ width: "100%", height: "100vh" }}>
      <p>To get your profile details: </p><button onClick={getData}>Click me</button>
        {profileData && <div>
              <p>Profile name: {profileData.profile_name}</p>
              <p>About me: {profileData.about_me}</p>
            </div>}
      <Form
        formId="1"
        formObj={{
          blocks: [
            {
              name: "welcome-screen",
              id: "jg1401r",
              attributes: {
                label: "Welcome to our survey",
                description: "This is just a description",
                attachment: {
                  type: "image",
                  url:
                    "https://quillforms.com/wp-content/uploads/2022/01/4207-ai-1.jpeg"
                }
              }
            },
            {
              name: "short-text",
              id: "kd12edg",
              attributes: {
                required: true,
                label: "Let's start with your name"
              }
            },
            {
              name: "number",
              id: "wer3qdkdb",
              attributes: {
                required: true,
                label: "Great {{field:kdsfkdg}}, can you type your age?"
              }
            },
            {
              name: "long-text",
              id: "m35612edg",
              attributes: {
                required: true,
                label: "Type a brief about yourself!"
              }
            },
            {
              name: "date",
              id: "a213rsew",
              attributes: {
                required: true,
                label: "Please type your birth of date!"
              }
            },
            {
              name: "email",
              id: "iqfrqwr13r",
              attributes: {
                required: true,
                label: "Thanks {{field:kdsfkdg}}, please insert your email!"
              }
            },
            {
              name: "dropdown",
              id: "nb913rqw",
              attributes: {
                required: true,
                label: "Please select one choice",
                choices: [
                  {
                    label: "Choice 1",
                    value: "choice-1"
                  },
                  {
                    label: "Choice 2",
                    value: "choice-2"
                  },
                  {
                    label: "Choice 2",
                    value: "choice-3"
                  }
                ]
              }
            },
            {
              name: "multiple-choice",
              id: "gqr1294c",
              attributes: {
                required: true,
                multiple: true,
                verticalAlign: false,
                label: "Which subjects do you love the most?",
                choices: [
                  {
                    label: "Physics",
                    value: "physics"
                  },
                  {
                    label: "Math",
                    value: "math"
                  },
                  {
                    label: "English",
                    value: "english"
                  },
                  {
                    label: "Biology",
                    value: "biology"
                  }
                ]
              }
            },
            {
              name: "statement",
              id: "g91imf1023",
              attributes: {
                label: "You are doing great so far!",
                buttonText: "Continue",
                quotationMarks: true
              }
            },
            {
              name: "website",
              id: "bv91em9123",
              attributes: {
                required: true,
                multiple: true,
                label: "Please insert your website url!"
              }
            }
          ],
          settings: {
            animationDirection: "vertical",
            disableWheelSwiping: false,
            disableNavigationArrows: false,
            disableProgressBar: false
          },
          theme: {
            font: "Roboto",
            buttonsBgColor: "#9b51e0",
            logo: {
              src: ""
            },
            questionsColor: "#000",
            answersColor: "#0aa7c2",
            buttonsFontColor: "#fff",
            buttonsBorderRadius: 25,
            errorsFontColor: "#fff",
            errorsBgColor: "#f00",
            progressBarFillColor: "#000",
            progressBarBgColor: "#ccc"
          }
        }}
        onSubmit={(data, { completeForm, setIsSubmitting }) => {
          setTimeout(() => {
            setIsSubmitting(false);
            completeForm();
          }, 500);
        }}
      />
    </div>
  );
};

export default App;
