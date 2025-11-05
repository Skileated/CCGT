import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { interpolateTurbo } from 'd3-scale-chromatic';
import { GraphData } from '../api';

interface GraphVizProps {
  graph: GraphData;
}

export default function GraphViz({ graph }: GraphVizProps) {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !graph.nodes.length) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = 600;
    const height = 400;
    svg.attr('width', width).attr('height', height);

    // Create force simulation
    const simulation = d3
      .forceSimulation(graph.nodes as any)
      .force(
        'link',
        d3
          .forceLink(graph.edges)
          .id((d: any) => d.id)
          .distance((d: any) => 140 - d.weight * 80)
          .strength(0.3)
      )
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(20));

    // Create edges
    const link = svg
      .append('g')
      .selectAll('line')
      .data(graph.edges)
      .enter()
      .append('line')
      .attr('stroke', (d: any) => {
        if (d.reason) return '#ef4444';
        const v = Math.max(0, Math.min(1, d.weight));
        return interpolateTurbo(v);
      })
      .attr('stroke-width', (d: any) => Math.max(1, d.weight * 2.5))
      .attr('stroke-opacity', 0.65);

    // Create nodes
    const node = svg
      .append('g')
      .selectAll('circle')
      .data(graph.nodes)
      .enter()
      .append('circle')
      .attr('r', 0)
      .attr('fill', (d: any) => {
        const val = (d.importance_score ?? (1 - (d.entropy ?? 0))) as number;
        const clamped = Math.max(0, Math.min(1, val));
        return interpolateTurbo(clamped);
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .call(
        d3
          .drag<any, any>()
          .on('start', dragstarted)
          .on('drag', dragged)
          .on('end', dragended)
      );

    // Animate node entry
    node
      .transition()
      .duration(600)
      .attr('r', (d: any) => 8 + (d.importance_score || 0.5) * 8)
      .ease(d3.easeCubicOut);

    // Add labels
    const label = svg
      .append('g')
      .selectAll('text')
      .data(graph.nodes)
      .enter()
      .append('text')
      .text((d: any) => `S${d.id + 1}`)
      .attr('font-size', '10px')
      .attr('dx', 12)
      .attr('dy', 4)
      .attr('fill', '#374151');

    // Tooltip
    const tooltip = d3
      .select('body')
      .append('div')
      .style('position', 'absolute')
      .style('padding', '8px')
      .style('background', 'rgba(0, 0, 0, 0.8)')
      .style('color', 'white')
      .style('border-radius', '4px')
      .style('font-size', '12px')
      .style('pointer-events', 'none')
      .style('opacity', 0)
      .style('z-index', 1000);

    node
      .on('mouseover', (event, d: any) => {
        tooltip.transition().duration(200).style('opacity', 1);
        tooltip
          .html(
            `<strong>Sentence ${d.id + 1}</strong><br/>${d.text_snippet}<br/>Entropy: ${d.entropy?.toFixed(3) || 'N/A'}`
          )
          .style('left', event.pageX + 10 + 'px')
          .style('top', event.pageY - 10 + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(200).style('opacity', 0);
      });

    link
      .on('mouseover', (event, d: any) => {
        tooltip.transition().duration(200).style('opacity', 1);
        tooltip
          .html(
            `Weight: ${d.weight.toFixed(3)}<br/>${d.discourse_marker ? `Discourse: ${d.discourse_marker}<br/>` : ''}${d.reason || ''}`
          )
          .style('left', event.pageX + 10 + 'px')
          .style('top', event.pageY - 10 + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(200).style('opacity', 0);
      });

    // Smoothly animate link positions
    link
      .transition()
      .duration(500)
      .ease(d3.easeCubicOut);

    // Update positions on simulation tick
    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);

      label.attr('x', (d: any) => d.x).attr('y', (d: any) => d.y);
    });

    function dragstarted(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event: any, d: any) {
      d.fx = event.x;
      d.fy = event.y;
    }

    function dragended(event: any, d: any) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }

    // Cleanup
    return () => {
      simulation.stop();
      tooltip.remove();
    };
  }, [graph]);

  return (
    <div className="w-full overflow-auto">
      <svg ref={svgRef} className="w-full border border-gray-200 rounded"></svg>
      <div className="mt-4 text-sm text-gray-600">
        <p>• Drag nodes to rearrange</p>
        <p>• Hover over nodes/edges for details</p>
        <p>• Red edges indicate disruptions</p>
      </div>
    </div>
  );
}

