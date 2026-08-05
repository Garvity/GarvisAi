import React, { useState ,useEffect} from "react";
import Markdown from "react-markdown";
import { Copy, ExternalLink, X, Check } from "lucide-react";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function MessageBubble({ role, content, images, file }) {
  const isUser = role === "user";
  const [lightBox, setLightBox] = useState(null);
  const [copiedCode, setCopiedCode] = useState("");
  const copyCode = async (code) => {
    await navigator.clipboard.writeText(code);
    setCopiedCode(code);
    setTimeout(() => {
      setCopiedCode("");
    }, 2000);
  };
  useEffect(() => {
    return () => {
      if (file?.preview) {
        URL.revokeObjectURL(file.preview);
      }
    };
  }, [file]);
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`w-fit max-w-[92vw] md:max-w-[72%] px-4 py-2.5 rounded-2xl break-words overflow-hidden leading-relaxed ${
          isUser
            ? "bg-gradient-to-br from-indigo-500 to-violet-700 text-white rounded-tr-sm"
            : " text-slate-200 rounded-tl-sm"
        }`}
      >
        {file && (
          <div className="mb-3">
            {file.type.startsWith("image/") ? (
              <img
                src={file.preview}
                alt={file.name}
                onClick={() => setLightBox(file.preview)}
                className="w-52 rounded-xl border border-white/10 cursor-pointer hover:opacity-90"
              />
            ) : (
              <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-white/5 px-3 py-3">
                <div className="text-red-400">📄</div>

                <div className="flex flex-col">
                  <span className="text-sm">{file.name}</span>
                  <span className="text-xs text-slate-400">
                    {(file.size / 1024).toFixed(1)} KB
                  </span>
                </div>
              </div>
            )}
          </div>
        )}

        {(() => {
          const mdComponents = {
            h1: ({ children }) => (
              <h1 className="text-2xl font-bold mt-5 mb-3">{children}</h1>
            ),
            h2: ({ children }) => (
              <h2 className="text-xl font-semibold mt-4 mb-2">{children}</h2>
            ),
            h3: ({ children }) => (
              <h3 className="text-lg font-semibold mt-3 mb-2">{children}</h3>
            ),
            p: ({ children }) => (
              <p className="mb-3 whitespace-pre-wrap break-words">{children}</p>
            ),
            ul: ({ children }) => (
              <ul className="list-disc pl-5 space-y-1 my-2">{children}</ul>
            ),
            ol: ({ children }) => (
              <ol className="list-decimal pl-5 space-y-1 my-2">{children}</ol>
            ),
            blockquote: ({ children }) => (
              <blockquote className="border-l-4 border-indigo-500 pl-4 italic my-2">
                {children}
              </blockquote>
            ),
            code: ({ children }) => (
              <code className="bg-white/10 px-1 py-[2px] rounded text-sm">
                {children}
              </code>
            ),
            pre: ({ children }) => (
              <pre className="bg-white/5 p-3 rounded my-2 overflow-x-auto">
                <code>{children}</code>
              </pre>
            ),
            table: ({ children }) => (
              <div className="overflow-x-auto my-4">
                <table className="min-w-full border border-white/10">
                  {children}
                </table>
              </div>
            ),
            th: ({ children }) => (
              <th className="border border-white/10 bg-white/5 px-3 py-2 text-left">
                {children}
              </th>
            ),
            td: ({ children }) => (
              <td className="border border-white/10 px-3 py-2">{children}</td>
            ),
            a: ({ href, children }) => (
              <a
                href={href}
                target="_blank"
                rel="noreferrer"
                className="text-indigo-400 underline inline-flex items-center gap-1"
              >
                {children}
                <ExternalLink size={14} />
              </a>
            ),
            // eslint-disable-next-line no-dupe-keys
            code: ({ className, children }) => {
              const value = String(children)
                .replace(/^\s*```[^\n]*\n/, "")
                .replace(/\n```\s*$/, "")
                .trim();
              if (!className) {
                return (
                  <code className="px-1.5 py-0.5 rounded bg-white/10 text-indigo-300">
                    {value}
                  </code>
                );
              }
              const language = className?.replace("language-", "") || "";

              return (
                <div className="my-4 overflow-hidden rounded-xl border border-white/10 bg-[#111318]">
                  <div className="flex items-center justify-between bg-[#1b1d24] border-b border-white/10 px-4 py-2">
                    <span className="uppercase text-xs text-slate-400">
                      {language}
                    </span>
                    <button
                      className="flex items-center gap-1 text-xs"
                      onClick={() => copyCode(value)}
                    >
                      {copiedCode == value ? (
                        <>
                          <Check size={14} />
                          Copied
                        </>
                      ) : (
                        <>
                          <Copy size={14} />
                          Copy
                        </>
                      )}
                    </button>
                  </div>
                  <SyntaxHighlighter
                    language={language}
                    style={oneDark}
                    wrapLongLines
                    showLineNumbers
                    customStyle={{
                      margin: 0,
                      padding: "16px",
                      backgroundColor: "#0d1117",
                      fontSize: "13px",
                    }}
                  >
                    {value}
                  </SyntaxHighlighter>
                </div>
              );
            },
            img: ({ src }) => {
              if (!src) return null;
              return (
                <img
                  src={src}
                  onClick={() => setLightBox(src)}
                  loading="lazy"
                  onError={(e) => e.currentTarget.remove()}
                  className="w-40 h-28 rounded-xl object-cover border border-white/10 cursor-zoom-in hover:opacity-90 transition"
                />
              );
            },
          };

          return (
            <Markdown remarkPlugins={[remarkGfm]} components={mdComponents}>
              {content}
            </Markdown>
          );
        })()}
        {images.length > 0 && (
          <div className="flex flex-wrap gap-3 mt-4">
            {images.map((img, i) => (
              <img
                key={i}
                src={img}
                onClick={() => setLightBox(img)}
                loading="lazy"
                onError={(e) => e.currentTarget.remove()}
                className="w-40 h-28 rounded-xl object-cover border border-white/10 cursor-zoom-in hover:opacity-90 transition"
                alt={`Image ${i + 1}`}
              />
            ))}
          </div>
        )}
      </div>
      {lightBox && (
        <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-6">
          <button
            className="absolute top-5 right-5 text-white/80 p-2 bg-white/10 hover:text-white rounded-full transition"
            onClick={() => setLightBox(null)}
          >
            <X />
          </button>
          <img
            src={lightBox}
            alt="Lightbox"
            className="max-w-[90vw] max-h-[85vh] rounded-2xl border border-white/10 shadow-2xl object-contain"
          />
        </div>
      )}
    </div>
  );
}

export default MessageBubble;
