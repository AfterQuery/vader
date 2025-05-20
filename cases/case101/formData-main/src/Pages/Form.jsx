import React from "react";
import { AiOutlineArrowRight } from "react-icons/ai";
import { RxCross1 } from "react-icons/rx";

const Form = () => {
  const onHandleFormSubmit = (data) => {};
  return (
    <div className="flex h-screen w-screen justify-center bg-surface-BG">
      <div className="my-6 w-1/2 rounded-lg bg-[#fff]">
        <div className="mx-6 mt-6 flex justify-between">
          <div className="flex gap-3">
            <button className="bg-[#F8F9FD] text-[#9DB4E6] px-2 text-[1rem]">{`<`}</button>
            <button className="bg-[#F8F9FD] text-[#9DB4E6] px-2 text-[1rem]">{`>`}</button>
          </div>
          <button className="bg-[#F8F9FD] text-[#9DB4E6] px-2 text-[1rem]">
            <RxCross1 />
          </button>
        </div>
        <form className="flex flex-col gap-4">
          <div className="ml-[15%] mr-[13%] mt-[6%]">
            <div className="flex flex-col gap-1 mb-12">
              <label
                htmlFor="campaignName"
                className="font-inter text-[1.4rem] font-[400] leading-[1.6rem] text-[#507AD3] flex"
              >
                <div className="flex items-center gap-2 ml-[-2.4rem] justify-center mr-2">
                  <h1 className="text-[1.1rem] font-inter font-[200]">1</h1>
                  <AiOutlineArrowRight size={15} />
                </div>
                Drop full name here *
              </label>
              <p className="font-inter mb-2 text-[1.125rem] font-[200] text-[#5A81D9] opacity-[0.7]">
                Add your email below to get notified as soon as it.
              </p>
              <input
                id="campaignName"
                placeholder="Rushil jha"
                // {...register("campaignName")}
                className="placeholder-[#b1c2e8] h-11 text-[#507AD3] font-inter text-[1.5rem]  border-b border-gray-300  focus:border-blue-500  focus:outline-none"
                required={true}
              />
            </div>
            <div className="flex flex-col gap-1 mb-12">
              <label
                htmlFor="campaignName"
                className="font-inter text-[1.4rem] font-[400] leading-[1.6rem] text-[#507AD3] flex"
              >
                <div className="flex items-center gap-2 ml-[-2.4rem] justify-center mr-2">
                  <h1 className="text-[1.1rem] font-inter font-[200]">2</h1>
                  <AiOutlineArrowRight size={15} />
                </div>
                Linkedin URL *
              </label>
              <p className="font-inter mb-2 text-[1.125rem] font-[200] text-[#5A81D9] opacity-[0.7]">
                Add your email below to get notified as soon as it.
              </p>
              <input
                id="campaignName"
                placeholder="https://yourlinkedin"
                // {...register("campaignName")}
                className="placeholder-[#b1c2e8] h-11 text-[#507AD3] font-inter text-[1.5rem]  border-b border-gray-300  focus:border-blue-500  focus:outline-none"
                required={true}
              />
            </div>
            <div className="flex flex-col gap-1 mb-12">
              <label
                htmlFor="campaignName"
                className="font-inter text-[1.4rem] font-[400] leading-[1.6rem] text-[#507AD3] flex"
              >
                <div className="flex items-center gap-2 ml-[-2.4rem] justify-center mr-2">
                  <h1 className="text-[1.1rem] font-inter font-[200]">3</h1>
                  <AiOutlineArrowRight size={15} />
                </div>
                Your work email address *
              </label>
              <p className="font-inter mb-2 text-[1.125rem] font-[200] text-[#5A81D9] opacity-[0.7]">
                Add your email below to get notified as soon as it.
              </p>
              <input
                id="campaignName"
                placeholder="rushil@atoms.so"
                // {...register("campaignName")}
                className="placeholder-[#b1c2e8] h-11 text-[#507AD3] font-inter text-[1.5rem]  border-b border-gray-300  focus:border-blue-500  focus:outline-none"
                required={true}
              />
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Form;
