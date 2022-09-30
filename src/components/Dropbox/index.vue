<template>
  <div v-if="isExternal" :style="styleExternalIcon" class="svg-external-icon svg-icon" v-on="$listeners" />
  <svg v-else :class="svgClass" aria-hidden="true" v-on="$listeners">
    <use :xlink:href="iconName" />
  </svg>
</template>

<script>
// doc: https://panjiachen.github.io/vue-element-admin-site/feature/component/svg-icon.html#usage
import { isExternal } from '@/utils/validate'
import loadable from "@loadable/component";
import * as React from "react";
import { useState } from "react";
import { Dataset } from "src/common/entities";

declare global {
  interface Window {
    Dropbox: {
      isBrowserSupported: () => boolean;
      choose: (options: unknown) => void;
    };
  }
}

const AsyncContent = loadable(
  () =>
    /*webpackChunkName: 'DropboxChooser/Content' */ import(
      "src/components/DropboxChooser/components/Content"
    )
);

export interface DropboxFile {
  link: string;
  name: string;
}

export type UploadingFile = DropboxFile & Partial<Dataset>;

const UPLOAD_SIZE_LIMIT_BYTES = 30 * 2 ** 30; // 30GB

const DROPBOX_OPTIONS = {
  extensions: [".h5ad"],
  sizeLimit: UPLOAD_SIZE_LIMIT_BYTES,
};

export interface Props {
  onUploadFile: (newFile: UploadingFile) => void;
  children: React.ReactElement;
}

const DropboxChooser = ({ children, onUploadFile }: Props): JSX.Element => {
  if (!React.Children.only(children)) {
    throw Error("DropboxChooser expects only one child");
  }

  const [isContentShown, setIsContentShown] = useState(false);

  const handleMouseOver = () => {
    setIsContentShown(true);
  };

  const handleClick = () => {
    if (!window.Dropbox.isBrowserSupported()) {
      alert("Sorry, your browser does not support Dropbox upload :(");
    }

    const options = {
      ...DROPBOX_OPTIONS,
      success(files: DropboxFile[] = []) {
        onUploadFile({ id: "", link: files[0].link, name: files[0].name });
      },
    };

    window.Dropbox.choose(options);
  };

  return (
    <>
      {React.cloneElement(children, {
        onClick: handleClick,
        onMouseOver: handleMouseOver,
      })}
      {isContentShown && <AsyncContent />}
    </>
  );
};

export default {
  name: 'DropboxChooser',
  props: {
    iconClass: {
      type: String,
      required: true
    },
    className: {
      type: String,
      default: ''
    }
  },
  computed: {
    isExternal() {
      return isExternal(this.iconClass)
    },
    iconName() {
      return `#icon-${this.iconClass}`
    },
    svgClass() {
      if (this.className) {
        return 'svg-icon ' + this.className
      } else {
        return 'svg-icon'
      }
    },
    styleExternalIcon() {
      return {
        mask: `url(${this.iconClass}) no-repeat 50% 50%`,
        '-webkit-mask': `url(${this.iconClass}) no-repeat 50% 50%`
      }
    }
  }
}
</script>

<style scoped>
.svg-icon {
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  fill: currentColor;
  overflow: hidden;
}

.svg-external-icon {
  background-color: currentColor;
  mask-size: cover!important;
  display: inline-block;
}
</style>
