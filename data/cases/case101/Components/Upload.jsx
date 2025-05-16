import React, { useState, useRef } from "react";
import { useValues } from "../context";
const Upload = ({question}) => {
  const [image, setImage] = useState(null);
  const [onDrag, setOnDrag] = useState(false);
  const imageSelect = useRef();


  const {
    formData,
            setFormData,
            error,
            setError,
            allErrors,
            setAllErrors,
            handleInputChange,
            handleOptionClick,
            getCurrentQuestions ,
            currentStep, setCurrentStep,
            questionsPerStep, setQuestionsPerStep,
            totalSteps,


  } = useValues();
  console.log(image);


  const handleDrop = (e) => {
    e.preventDefault();
    console.log(e.target.files[0].size)
    if(e.target.files[0].size > 5 * 1024 * 1024){
      console.log("big-sizee")
      allErrors[question.id] = true;
    }else{
      setImage(e.target.files[0])
   setOnDrag(false);
    }
   
  };



  console.log("valuee",image)

  const handleDrag = (e) => {
    e.preventDefault();
    setOnDrag(true);
  };
  return (
    <div
      className={` cursor-pointer h-[114px] gap-2 flex flex-col justify-center items-center rounded-[6px] ${
        image
          ? "bg-blue-300 bg-opacity-[0.3] border-[#4A7BE5] border-2"
          : "border-[#CED9F2] border-1 bg-[#F8FAFD]"
      } 
    border ${onDrag ? "border-dashed" : "border-solid"} `}
      onDragOver={(e) => handleDrag(e)}
      onDrop={(e) => handleDrop(e)}
      onClick={() => imageSelect.current.click()}
    >
      {image ? (
        <div className="flex flex-col  justify-center gap-2 items-center  text-[0.7rem] opacity-[0.5]">
          <img className="w-[15px] h-[15px]" src={URL.createObjectURL(image)} />
          <p>{image.name}</p>
        </div>
      ) : (
        <div className="flex flex-col justify-center items-center">
          <img src="upload.svg" />
          <p className="text-[#507AD3] text-[1.12rem]">
            Upload a file{" "}
            <span className="opacity-[0.7]">or drag and drop</span>{" "}
          </p>
        </div>
      )}

      <input
        type="file"
        onChange={(e) => handleDrop(e)}
        ref={imageSelect}
        accept="image/*"
        hidden
      />
    </div>
  );
};

export default Upload;
