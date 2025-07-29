from rkllm.api import RKLLM

# AttributeError: module 'pyarrow' has no attribute 'PyExtensionType'. Did you mean: 'ExtensionType'?
# pip install pyarrow==20.0.0

rkllm = RKLLM()
ret = rkllm.load_huggingface( model = 'QVikhr-3-4B-Instruction' )

if ret != 0:
    print('Load model failed!')

ret = rkllm.build(
 do_quantization=True,
 optimization_level=1,
 quantized_dtype='w8a8',
 quantized_algorithm="normal",
 num_npu_core=3,
 extra_qparams=None,
 dataset="quant_data.json",
 hybrid_rate=0,
 target_platform='rk3588')
if ret != 0:
    print('Buildmodel failed!')

ret = rkllm.export_rkllm(export_path='qvikhr.rkllm')

if ret != 0:
    print('Export model failed!')

print("Done")
